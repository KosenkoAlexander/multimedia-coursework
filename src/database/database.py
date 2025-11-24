

class DatabaseConnector:
    def __init__(self):
        pass #...

    def search_books_by_authors(authors): # authors is a list that may have string name or string surname or tuple (name, surname) or tuple (surname, name)
        pass # returns book name list

    def search_books_by_genres(genres): # genres is list of genres
        pass # returns book name list that have at least one of these genres
    
    def search_libraries_with_book(book):
        pass # return list of tuples (library, address, is_book_available)

    def get_book(name):
        pass #return tuple (book, list_of_authors, list_of_genres)

    def search_shops_with_book(book):
        pass # return list of tuples (shop, address, price)

    def get_genre_list():
        pass # just return list of all possible genre names

    def get_specialty_list():
        pass # just return list of all possible specialties

    def get_libraries_by_specialties(specialties):
        pass # list of (library, address) where library has at least one of listed specialties
    
    def get_shops_by_specialties(specialties):
        pass # list of (shop, address) where shop has at least one of listed specialties
