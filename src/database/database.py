import os
import psycopg2

class DatabaseConnector:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.conn.autocommit = True
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


    #SEARCH

    def search_books_by_authors(self, authors):
        """Return list of [book.id, book.name]"""
        if not self.conn: return []

        query = """
                SELECT DISTINCT b.id, b.name
                FROM book b
                         JOIN book_author ba ON b.id = ba.book
                         JOIN author a ON a.id = ba.author
                WHERE \
                """
        conditions = []
        params = []

        for author in authors:
            if isinstance(author, tuple) and len(author) == 2:
                conditions.append(
                    "((a.name ILIKE %s AND a.surname ILIKE %s) OR (a.name ILIKE %s AND a.surname ILIKE %s))")
                params.extend([author[0], author[1], author[1], author[0]])
            elif isinstance(author, str):
                parts = author.split()
                if len(parts) >= 2:
                    p1, p2 = parts[0], parts[1]
                    conditions.append(
                        "((a.name ILIKE %s AND a.surname ILIKE %s) OR (a.name ILIKE %s AND a.surname ILIKE %s))")
                    params.extend([p1, p2, p2, p1])
                else:
                    conditions.append("(a.name ILIKE %s OR a.surname ILIKE %s)")
                    params.extend([author, author])

        if not conditions: return []

        full_query = query + " OR ".join(conditions)

        with self.conn.cursor() as cur:
            cur.execute(full_query, params)
            return cur.fetchall() #[row[0] for row in cur.fetchall()]

    def search_books_by_genres(self, genres):
        """Return list of [book.id, book.name]"""
        if not self.conn: return []
        query = """
                SELECT DISTINCT b.id, b.name
                FROM book b
                         JOIN book_genre bg ON b.id = bg.book
                         JOIN genre g ON g.id = bg.genre
                WHERE g.name = ANY (%s) \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (genres,))
            return cur.fetchall() #[row[0] for row in cur.fetchall()]

    def search_books_by_genres_or_authors(self, genres, authors):

        if not self.conn:
            return []

        if isinstance(genres, str): genres = [genres]
        if isinstance(authors, str): authors = [authors]

        query = """
                SELECT b.name, \
                       ARRAY_AGG(DISTINCT a.name || ' ' || a.surname) as authors_list, \
                       ARRAY_AGG(DISTINCT g.name)                     as genres_list
                FROM book b
                         LEFT JOIN book_author ba ON b.id = ba.book
                         LEFT JOIN author a ON ba.author = a.id
                         LEFT JOIN book_genre bg ON b.id = bg.book
                         LEFT JOIN genre g ON bg.genre = g.id
                GROUP BY b.id, b.name
                HAVING
                -- Оператор && перевіряє, чи є перетин між масивами (чи є спільні елементи)
                    ARRAY_AGG(g.name)::varchar[] && %s:: varchar []
                    OR
                    ARRAY_AGG(a.surname):: varchar [] && %s:: varchar [] \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (genres, authors))
            return cur.fetchall()

    def search_libraries_with_book(self, book_name):

        if not self.conn:
            return []

        query = """
                SELECT l.name, \
                       l.address, \
                       bl.available, \
                       bl.link
                FROM libraries l
                         JOIN book_library bl ON l.id = bl.library
                         JOIN book b ON b.id = bl.book
                WHERE b.name ILIKE %s \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (book_name,))
            return cur.fetchall()

    def search_shops_with_book(self, book_name):
        if not self.conn: return []

        query = """
                SELECT s.name, s.address, bs.price, bs.link
                FROM shops s
                         JOIN book_shop bs ON s.id = bs.shop
                         JOIN book b ON b.id = bs.book
                WHERE b.name ILIKE %s \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (book_name,))
            # row[0] - name, row[1] - address, row[2] - price, row[3] - link
            return [(row[0], row[1], float(row[2]), row[3]) for row in cur.fetchall()]

    def find_user_by_id(self, id):
        # Повертає tuple (id, username, email, password_hash, is_admin) або None
        if not self.conn: return None

        query = """
                SELECT id, username, email, password_hash, is_admin
                FROM users
                WHERE id = %s \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (id,))
            return cur.fetchone()

    def find_user_by_username(self, username):
        if not self.conn: return None

        query = """
                SELECT id, username, email, password_hash, is_admin
                FROM users
                WHERE username = %s \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (username,))
            return cur.fetchone()

    def find_user_by_email(self, email):
        if not self.conn: return None

        query = """
                SELECT id, username, email, password_hash, is_admin
                FROM users
                WHERE email = %s \
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (email,))
            return cur.fetchone()


    # GET

    def get_book_like(self, name):
        if not self.conn: return None
        try:
            query = "SELECT id, name, pages FROM book WHERE name ILIKE %s LIMIT 1"

            search_pattern = f"%{name}%"

            with self.conn.cursor() as cur:
                cur.execute(query, (search_pattern,))
                result = cur.fetchone()
                return result
        except Exception as e:
            print(f"Error searching book like '{name}': {e}")
            return None

    def get_all_authors(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, surname FROM author ORDER BY surname")
            return cur.fetchall()

    def get_all_genres(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM genre ORDER BY name")
            return cur.fetchall()

    def get_all_shops(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM shops ORDER BY name")
            return cur.fetchall()

    def get_all_libraries(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM libraries ORDER BY name")
            return cur.fetchall()

    def get_book(self, name):
        """return Book name, authors, genres, id"""
        if not self.conn: return None
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM book WHERE name ILIKE %s", (name,))
            book_data = cur.fetchone()

            if not book_data: return None

            book_id, book_real_name = book_data

            cur.execute(
                "SELECT a.name || ' ' || a.surname FROM author a JOIN book_author ba ON a.id = ba.author WHERE ba.book = %s",
                (book_id,))
            authors = [row[0] for row in cur.fetchall()]

            cur.execute("SELECT g.name FROM genre g JOIN book_genre bg ON g.id = bg.genre WHERE bg.book = %s",
                        (book_id,))
            genres = [row[0] for row in cur.fetchall()]

            return (book_real_name, authors, genres, book_id)

    def get_genre_list(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM genre")
            return [row[0] for row in cur.fetchall()]

    def get_specialty_list(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT name FROM specialty")
            return [row[0] for row in cur.fetchall()]

    def get_libraries_by_specialties(self, specialties):
        if not self.conn: return []
        query = """
                SELECT DISTINCT l.name, l.address
                FROM libraries l
                         JOIN library_specialty ls ON l.id = ls.library
                         JOIN specialty s ON s.id = ls.specialty
                WHERE s.name = ANY (%s) \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (specialties,))
            return cur.fetchall()

    def get_shops_by_specialties(self, specialties):
        if not self.conn: return []
        query = """
                SELECT DISTINCT sh.name, sh.address
                FROM shops sh
                         JOIN shop_specialty ss ON sh.id = ss.shop
                         JOIN specialty s ON s.id = ss.specialty
                WHERE s.name = ANY (%s) \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (specialties,))
            return cur.fetchall()

    def get_all_books(self):
        #Повертає список всіх книг для відображення у формі
        if not self.conn: return []
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name FROM book ORDER BY name")
            return cur.fetchall()

    def get_all_users(self):
        if not self.conn: return []
        with self.conn.cursor() as cur:
            # Сортуємо по ID
            cur.execute("SELECT id, username, email, is_admin FROM users ORDER BY id")
            return cur.fetchall()

    def get_user_by_username(self, username):
        #Шукає користувача за username і повертає кортеж даних або None
        if not self.conn: return None

        query = """
                SELECT id, username, email, password_hash, is_admin
                FROM users
                WHERE username = %s
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (username,))
            return cur.fetchone()

    def get_user_by_id(self, user_id):
        if not self.conn: return None

        query = """
                SELECT id, username, email, password_hash, is_admin
                FROM users
                WHERE id = %s
                """

        with self.conn.cursor() as cur:
            cur.execute(query, (user_id,))
            return cur.fetchone()

    # ADD

    def add_user(self, username, email, password_hash, is_admin=False):
        #Додає користувача та повертає його ID.
        if not self.conn: return None

        query = """
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (%s, %s, %s, %s) RETURNING id \
                """

        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (username, email, password_hash, is_admin))
                new_id = cur.fetchone()[0]
                self.conn.commit()
                return new_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding user: {e}")
            return None

    def add_book_to_shop(self, book_id, shop_id, price, link):
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO book_shop (book, shop, price, link)
                            VALUES (%s, %s, %s, %s)
                            """, (book_id, shop_id, price, link))
        except Exception as e:
            print(f"Error adding to shop: {e}")

    def add_book_to_library(self, book_id, library_id, link):
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO book_library (book, library, available, link)
                            VALUES (%s, %s, true, %s)
                            """, (book_id, library_id, link))
        except Exception as e:
            print(f"Error adding to library: {e}")


    # CHANGE

    def change_user_username(self, id, new_username):
        if not self.conn: return

        query = "UPDATE users SET username = %s WHERE id = %s"

        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (new_username, id))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error changing username: {e}")

    def change_user_password_hash(self, id, new_password_hash):
        if not self.conn: return

        query = "UPDATE users SET password_hash = %s WHERE id = %s"

        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (new_password_hash, id))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error changing password: {e}")

    def change_user_is_admin(self, id):

        if not self.conn: return

        query = "UPDATE users SET is_admin = NOT is_admin WHERE id = %s"

        try:
            with self.conn.cursor() as cur:
                cur.execute(query, (id,))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error toggling admin status: {e}")


    # CREATE

    def create_book(self, name, pages):
        #Створює книгу і повертає її ID
        if not self.conn: return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO book (name, pages) VALUES (%s, %s) RETURNING id", (name, pages))
                book_id = cur.fetchone()[0]
                return book_id
        except Exception as e:
            print(f"Error creating book: {e}")
            return None

    def create_author(self, name, surname):
        #Створює автора і повертає його ID
        if not self.conn: return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO author (name, surname) VALUES (%s, %s) RETURNING id", (name, surname))
                author_id = cur.fetchone()[0]
                return author_id
        except Exception as e:
            print(f"Error creating author: {e}")
            return None


    # LINK

    def link_authors_to_book(self, book_id, author_ids):
        #Прив'язує список ID авторів до книги
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                for auth_id in author_ids:
                    cur.execute("INSERT INTO book_author (book, author) VALUES (%s, %s)", (book_id, auth_id))
        except Exception as e:
            print(f"Error linking authors: {e}")

    def link_genres_to_book(self, book_id, genre_ids):
        #Прив'язує список ID жанрів до книги
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                for g_id in genre_ids:
                    cur.execute("INSERT INTO book_genre (book, genre) VALUES (%s, %s)", (book_id, g_id))
        except Exception as e:
            print(f"Error linking genres: {e}")

    def link_books_to_author(self, author_id, book_ids):
        #Прив'язує список ID книг до автора (зворотна дія до link_authors_to_book)
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                for b_id in book_ids:
                    cur.execute("INSERT INTO book_author (book, author) VALUES (%s, %s)", (b_id, author_id))
        except Exception as e:
            print(f"Error linking books to author: {e}")


    # USER

    def username_exists(self, username):
        #Перевіряє, чи зайнятий username. Повертає True або False.
        if not self.conn: return False

        query = "SELECT 1 FROM users WHERE username = %s"

        with self.conn.cursor() as cur:
            cur.execute(query, (username,))
            return cur.fetchone() is not None

    def email_exists(self, email):
        #Перевіряє, чи зайнятий email
        if not self.conn: return False

        query = "SELECT 1 FROM users WHERE email = %s"

        with self.conn.cursor() as cur:
            cur.execute(query, (email,))
            return cur.fetchone() is not None


    #DELETE

    def delete_user(self, user_id):
        #Видаляє користувача за ID
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting user: {e}")

    def delete_book(self, book_id):
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM book WHERE id = %s", (book_id,))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting book: {e}")

    def delete_author(self, author_id):
        if not self.conn: return
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM author WHERE id = %s", (author_id,))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting author: {e}")


    #UPDATE

    def update_username(self, user_id, new_username):
        if not self.conn: return False
        try:
            query = "UPDATE users SET username = %s WHERE id = %s"
            with self.conn.cursor() as cur:
                cur.execute(query, (new_username, user_id))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating username: {e}")
            return False

    def update_password(self, user_id, password_hash):
        if not self.conn: return False
        try:
            query = "UPDATE users SET password_hash = %s WHERE id = %s"
            with self.conn.cursor() as cur:
                cur.execute(query, (password_hash, user_id))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False


#FAVOURITES

    def add_favorite(self, user_id, book_id):
        query = "INSERT OR IGNORE INTO favorites (user_id, book_id) VALUES (?, ?)"
        with self.conn.cursor() as cur:
            cur.execute(query, (user_id, book_id))
            self.conn.commit()

    def remove_favorite(self, user_id, book_id):
        query = "DELETE FROM favorites WHERE user_id = ? AND book_id = ?"
        with self.conn.cursor() as cur:
            cur.execute(query, (user_id, book_id))
            self.conn.commit()

    def get_user_favorites(self, user_id):
        #Отримує список всіх улюблених книг користувача з деталями про книгу
        query = """
                SELECT b.id, b.name, b.pages, b.cover_image
                FROM books b
                         JOIN favorites f ON b.id = f.book_id
                WHERE f.user_id = ? \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (user_id,))
            return cur.fetchall()

    def is_book_favorite(self, user_id, book_id):
        #Перевіряє, чи є конкретна книга в улюблених
        query = "SELECT 1 FROM favorites WHERE user_id = ? AND book_id = ?"
        with self.conn.cursor() as cur:
            cur.execute(query, (user_id, book_id))
            return cur.fetchone() is not None

# TEST
if __name__ == '__main__':

    DB_NAME = "postgres"
    USER = "postgres"
    PASSWORD = os.getenv("POSTGRES_PASS", "postgres")
    HOST = "localhost"

    print(" Connecting to database...")
    db = DatabaseConnector(DB_NAME, USER, PASSWORD, HOST)

    if db.conn:
        print(" Connection successful!\n")
        print("=" * 60)

        # Test 1
        print("\n [1] Searching books by authors:")
        authors_to_find = [
            "Einstein",  # Прізвище
            ("Charles", "Darwin"),  # Кортеж (Ім'я, Прізвище)
            "Knuth Donald"  # Переплутаний порядок слів у рядку
        ]
        books = db.search_books_by_authors(authors_to_find)
        for b in books:
            print(f"   - {b}")

        # Test 2
        print("\n [2] Searching books by genres (Biology & CS):")
        genres_to_find = ["Biology & Evolution", "Computer Science"]
        books_by_genre = db.search_books_by_genres(genres_to_find)
        for b in books_by_genre:
            print(f"   - {b}")

        # Test 3
        print("\n [3] Getting details for 'The Biosphere':")
        book_details = db.get_book("The Biosphere")
        if book_details:
            name, authors, genres = book_details
            print(f" Title: {name}")
            print(f" Authors: {', '.join(authors)}")
            print(f" Genres: {', '.join(genres)}")
        else:
            print(" Book not found")

        # Test 4
        print("\narchitectures [4] Libraries having 'Relativity: The Special and General Theory':")
        libraries = db.search_libraries_with_book("Relativity: The Special and General Theory")
        for lib in libraries:
            # lib = (Name, Address, Available)
            status = " Available" if lib[2] else " Taken"
            print(f"   - {lib[0]} ({lib[1]}) -> {status}")

        # Test 5
        print("\n [5] Shops selling 'Just for Fun: The Story of an Accidental Revolutionary':")
        shops = db.search_shops_with_book("Just for Fun: The Story of an Accidental Revolutionary")
        for shop in shops:
            # shop = (Name, Address, Price)
            print(f"   - {shop[0]}: {shop[2]} UAH/USD (at {shop[1]})")

        # Test 6
        print("\n [6] All Genres list:")
        print(f"   {db.get_genre_list()}")

        # Test 7
        print("\n [7] All Specialties list:")
        print(f"   {db.get_specialty_list()}")

        # Test 8
        print("\n [8] Libraries specializing in 'Academic Research':")
        specialty_libs = db.get_libraries_by_specialties(["Academic Research"])
        for lib in specialty_libs:
            print(f"   - {lib[0]} ({lib[1]})")

        # Test 9
        print("\n [9] Shops specializing in 'Foreign Literature':")
        specialty_shops = db.get_shops_by_specialties(["Foreign Literature"])
        for shop in specialty_shops:
            print(f"   - {shop[0]} ({shop[1]})")

        # Test 10
        books = db.search_books_by_genres_or_authors(["Physics"], ["Turing", "King"])
        for book in books:
            print(f" [10] Книга: {book[0]}")
            print(f"Автори: {book[1]}")
            print(f"Жанри: {book[2]}")
            print("-" * 20)

        # Test 11
        libs = db.search_libraries_with_book("Clean Code")
        for lib in libs:
            name, address, available, link = lib
            print(f" [11]  Бібліотека: {name}, Доступна: {available}")
            if link:
                print(f"Читати онлайн: {link}")
            else:
                print("Тільки паперова версія")

        # Test 12
        print("\n--- 12. ТЕСТ ПОШУКУ КНИГ (Жанр 'Physics' або автор 'Knuth') ---")
        books = db.search_books_by_genres_or_authors(["Physics"], ["Knuth"])
        for b in books:
            print(f" Назва: {b[0]} | Автори: {b[1]} | Жанри: {b[2]}")

        print("\n--- 13. ТЕСТ БІБЛІОТЕК (Книга 'Clean Code') ---")
        libs = db.search_libraries_with_book("Clean Code")
        for l in libs:
            status = "Доступна" if l[2] else "Зайнята"
            link = l[3] if l[3] else "Тільки фізична копія"
            print(f" {l[0]} ({l[1]}) -> {status} | Link: {link}")

        print("\n--- 14. ТЕСТ МАГАЗИНІВ (Книга 'A Brief History of Time') ---")
        shops = db.search_shops_with_book("A Brief History of Time")
        for s in shops:
            link = s[3] if s[3] else "Купівля в магазині"
            print(f" {s[0]} -> {s[2]}$ | Link: {link}")

#        print("\n--- 15. ТЕСТ КОРИСТУВАЧІВ ---")
#        # Додаємо тестового юзера
#        test_username = "test_student"
#        test_email = "student@university.com"
#        user_id = db.add_user(test_username, test_email, "hashed_secret_123")
#
#        if user_id:
#            print(f"16 Користувача створено з ID: {user_id}")
#
#            # Перевірка пошуку
#            u = db.find_user_by_id(user_id)
#            print(f" Знайдено по ID: {u[1]} (Admin: {u[4]})")
#
#            # Зміна імені
#            print("Змінюємо username на 'super_student'...")
#            db.change_user_username(user_id, "super_student")
#            u = db.find_user_by_username("super_student")
#            print(f"   Нове ім'я в БД: {u[1] if u else 'Error'}")
#
#            # Зміна прав адміна
#            print(" Робимо адміном...")
#            db.change_user_is_admin(user_id)
#            u = db.find_user_by_id(user_id)
#            print(f"   Тепер Admin: {u[4]}")
#
#        else:
#            print(" Не вдалося створити користувача (можливо, такий email/username вже існує).")
#
        print("\n" + "=" * 60)
        print(" Tests finished.")

    else:
        print(" Failed to connect. Please check your password/port.")