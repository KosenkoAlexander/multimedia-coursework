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

    def search_books_by_authors(self, authors):
        if not self.conn: return []

        query = """
                SELECT DISTINCT b.name
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
            return [row[0] for row in cur.fetchall()]

    def search_books_by_genres(self, genres):
        if not self.conn: return []
        query = """
                SELECT DISTINCT b.name
                FROM book b
                         JOIN book_genre bg ON b.id = bg.book
                         JOIN genre g ON g.id = bg.genre
                WHERE g.name = ANY (%s) \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (genres,))
            return [row[0] for row in cur.fetchall()]

    def search_books_by_genres_or_authors(self, genres, authors): #TODO return books that correspond to genres OR authors (so it may have wrong genres or wrong authors but not both), return as tuple (book, authors_list, genres_list)
        pass

    def search_libraries_with_book(self, book_name): #TODO add link as 4th tuple element (None if it is NULL in table (if book is in paper))
        if not self.conn: return []
        query = """
                SELECT l.name, l.address, bl.available
                FROM libraries l
                         JOIN book_library bl ON l.id = bl.library
                         JOIN book b ON b.id = bl.book
                WHERE b.name ILIKE %s \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (book_name,))
            return cur.fetchall()

    def get_book(self, name):
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

            return (book_real_name, authors, genres)

    def search_shops_with_book(self, book_name): #TODO add link as 4th tuple element (None if it is NULL in table (if book is in paper))
        if not self.conn: return []
        query = """
                SELECT s.name, s.address, bs.price
                FROM shops s
                         JOIN book_shop bs ON s.id = bs.shop
                         JOIN book b ON b.id = bs.book
                WHERE b.name ILIKE %s \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (book_name,))
            return [(row[0], row[1], float(row[2])) for row in cur.fetchall()]

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

    def find_user_by_id(self, id): #these 3 user finding methods must return tuple (id, username, email, password_hash, is_admin) if user exists else None
        pass #TODO

    def find_user_by_username(self, username):
        pass #TODO

    def find_user_by_email(self, email):
        pass #TODO

    def add_user(self, username, email, password_hash, is_admin = False):
        pass #TODO

    def change_user_username(self, id, new_username):
        pass #TODO

    def change_user_password_hash(self, id, new_password_hash):
        pass #TODO

    def change_user_is_admin(self, id):
        pass #TODO


# TEST
if __name__ == '__main__':

    DB_NAME = "postgres"
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"

    print(" Connecting to database...")
    db = DatabaseConnector(DB_NAME, USER, PASSWORD, HOST)

    if db.conn:
        print(" Connection successful!\n")
        print("="*60)

        # Test 1
        print("\n [1] Searching books by authors:")
        authors_to_find = [
            "Einstein",                  # Прізвище
            ("Charles", "Darwin"),       # Кортеж (Ім'я, Прізвище)
            "Knuth Donald"               # Переплутаний порядок слів у рядку
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

        print("\n" + "="*60)
        print(" Tests finished.")

    else:
        print(" Failed to connect. Please check your password/port.")
