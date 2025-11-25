# code written here will be responsible for answering users input

from enum import Enum
import datetime
from dialogues.text_processing import *
import re
from database.database import DatabaseConnector

class DialogueProcessor:
    def process_initial(self, text):
        text_l = text.lower()
        words = re.findall(word_regex, text_l)
        default_reply = 'Hello, how can I assist you? Say help if you need a quick tutorial'
        if not self.database_connector:
            default_reply += ' Unfortunately my database is not connected, so I have limited knowledge'
        if len(words)==0:
            return default_reply
        hello_detected = False
        for w in hello_words:
            if w in words:
                if len(words) == 1:
                    return default_reply 
                hello_detected = True
                break
        # add more hello extensions later
        return self.process_default(text)
        
    def process_default(self, text):
        text_l = text.lower()
        if re.match('goodbye.*', text_l):
            self.goodbye = True
            return 'Goodbye'
        elif book_desc:=re.search(r'(?:\bfind\b|\bsearch\s+for\b)(.*)(?:book)(.*)', text_l):
            self.book_specifiers = re.findall(word_regex, book_desc.group(1))
            book_description = book_desc.group(2)
            self.current_authors = []
            if authored := re.search(r'(?:\bauthored\s+by\b|\bwith\b.*\bauthors)(.*)', book_description):
                potential_authors = [s for s in re.findall(word_regex, authored.group(1)) if s!='and']
                if len(potential_authors)==0:
                    self.current_processor = self.process_clarify_authors
                    return 'Please clarify authors or say cancel to stop search'
                else:
                    return self.answer_for_nonempty_potential_authors(potential_authors)
            elif len(self.book_specifiers)>0:
                return self.answer_books_by_genres_only()
            else:
                self.current_processor = self.process_find_book
                return 'Please describe the book you want to find'
        elif library_desc:=re.search(r'(?:\bfind\b|\bsearch\b(?:\s+for\b)?)(.*)(?:librar(?:y|ies))(.*)', text_l):
            self.library_specifiers = [s for s in re.findall(word_regex, library_desc.group(1)) if s!='and']
            if close_to:=re.search(r'(?:\bnear\b|\bclose\b(?:\s+to\b)?)(.*)', library_desc.group(2)):
                if re.search(r'(?:\bme\b|(?:\bmy\b(?:home|house|location)))', close_to.group(1)):
                    return 'Address queries are not implemented yet' # implement
                else:
                    return 'Address queries are not implemented yet' # implement
            elif place_desc := re.search(r'(?:\bin\b)(.*)', library_desc.group(2)):
                if re.search(r'(?:\bmy\s+(?:town|city))', place_desc.group(1)):
                    return 'Address queries are not implemented yet' # implement
                else:
                    return 'Address queries are not implemented yet' # implement
            else:
                if len(self.library_specifiers)==0:
                    self.current_processor = self.process_find_library
                    return 'Describe the library you want to find'
                else:
                    return self.answer_libraries_by_specifiers()
        elif shop_desc:=re.search(r'(?:\bfind\b|\bsearch\b(?:\s+for\b)?)(.*)(?:shops?)(.*)', text_l):
            self.shop_specifiers = [s for s in re.findall(word_regex, shop_desc.group(1)) if s!='and']
            if close_to:=re.search(r'(?:\bnear\b|\bclose\b(?:\s+to\b)?)(.*)', shop_desc.group(2)):
                if re.search(r'(?:\bme\b|(?:\bmy\b(?:home|house|location)))', close_to.group(1)):
                    return 'Address queries are not implemented yet' # implement
                else:
                    return 'Address queries are not implemented yet' # implement
            elif place_desc := re.search(r'(?:\bin\b)(.*)', shop_desc.group(2)):
                if re.search(r'(?:\bmy\s+(?:town|city))', place_desc.group(1)):
                    return 'Address queries are not implemented yet' # implement
                else:
                    return 'Address queries are not implemented yet' # implement
            else:
                if len(self.shop_specifiers)==0:
                    self.current_processor = self.process_find_shop
                    return 'Describe the shop you want to find'
                else:
                    return self.answer_shops_by_specifiers()
        elif re.search(r'\b(list|get|describe|tell)\b.*\bgenre', text_l):
            genres = self.get_all_genres()
            if not genres:
                return 'Database connection issues, sorry'
            return 'The following genres are present in my database: '+', '.join(genres)
        elif re.search(r'\b(list|get|describe|tell)\b.*\bspecialt', text_l):
            specialties = self.get_all_specialties()
            if not specialties:
                return 'Database connection issues, sorry'
            return 'The following library and shop specialties are present in my database: '+', '.join(specialties)

        return 'Hello, your request was not recognised. If you need help, say help.'

    def process_clarify_authors(self, text):
        text_l = text.lower()
        if re.match(r'cancel\b', text_l):
            self.current_processor = self.process_default
            return 'Cancelled'
        potential_authors = [s for s in re.findall(word_regex, text_l) if s!='and']
        if len(potential_authors)==0:
            return 'Input unclear again, please repeat authors or cancel search'
        return self.answer_for_nonempty_potential_authors(potential_authors)

    def answer_for_nonempty_potential_authors(self, potential_authors):
        self.current_authors = []
        for i in range(len(potential_authors)//2):
            self.current_authors.append((potential_authors[2*i],potential_authors[2*i+1]))
        if len(potential_authors)%2:
            self.current_authors.append(potential_authors[-1])
        books = self.search_books()
        if len(books) == 0:
            self.current_processor = self.process_default
            return 'Seems like no books from this author is in database'
        else:
            self.current_processor = self.process_after_book_found
            self.current_books = books
            return 'The following books were found: '+', '.join(books) + '. Do you want me to search for them in libraries or shops?'

    def answer_books_by_genres_only(self):
        books = self.search_books()
        if not books:
            return 'There are problems with database connection'
        if len(books) == 0:
            self.current_processor = self.process_default
            return 'Seems like there are no books corresponding to the description'
        self.current_books = books
        self.current_processor = self.process_after_book_found
        return 'The following books were found: ' + ', '.join(books) + '. Do you want me to serach for them in librarier or shops?'

    def answer_book_name(self, name, none_if_negative = False):
        book = self.search_book_by_name(name)
        if not book:
            if none_if_negative:
                return None
            else:
                self.current_processor = self.process_default
                return 'Book with this name was not found'
        self.current_processor = self.process_after_book_found
        self.current_books = book
        return 'There is a book with name '+book[0]+' written by '+', '.join(book[1])+'. Want me to search it in shops or libraries?'

    def answer_libraries_by_specifiers(self):
        libraries = self.search_libraries()
        self.current_processor = self.process_default
        if len(libraries)==0:
            return 'No libraries with specified description found'
        return 'Libraries corresponding to description: '+', '.join([l[0]+', located at '+l[1] for l in libraries])

    def answer_shops_by_specifiers(self):
        shops = self.search_shops()
        self.current_processor = self.process_default
        if len(shops)==0:
            return 'No shops with specified description found'
        return 'Shops corresponding to description: '+', '.join([s[0]+', located at '+s[1] for s in shops])

    def process_find_book(self, text):
        text_l = text.lower()
        if text_l == 'cancel':
            self.current_processor = self.process_default
            return 'Cancelling search'
        if book_name:=re.search(r'(?:\bname\b).*(?:\bis\b)?(.*)', text_l):
            name = book_name.group(1)
            return self.answer_book_name(name)
        if authors_desc:=re.search(r'(?:authors?)(?:.*is|.*are)?(.*)', text_l):
            potential_authors = [s for s in re.findall(word_regex, authors_desc.group(1)) if s!='and']
            if len(potential_authors)==0:
                self.current_processor = self.process_clarify_authors
                return 'Could not understand authors, please repeat or say cancel to stop search'
            else:
                return self.answer_for_nonempty_potential_authors(potential_authors)
        elif genre_desc:=re.search(r'(?:genres?)(?:.*is|.*are)?(.*)', text_l):
            self.book_specifiers = re.findall(word_regex, genre_desc.group(1))
            if len(self.book_specifiers)>0:
                return self.answer_books_by_genres_only()
        return 'Description is not recognisable, please say book genres, book name or book authors, or say cancel if you want to stop searching'

    def process_after_book_found(self, text):
        text_l = text.lower()
        places_string = ''
        in_libraries = text_l == 'yes' or re.search(r'\blibrar', text_l)
        in_shops = text_l == 'yes' or re.search(r'\bshop', text_l)
        self.current_processor = self.process_default
        if not in_libraries and not in_shops:
            if text == 'no':
                return 'Stopping search'
            else:
                return 'Request not recognised'
        if in_libraries:
            libraries = self.search_libraries_by_books()
            places_string += ', '.join([l[0]+', located at '+l[1] for l in libraries])
        if in_shops:
            shops = self.search_shops_by_books()
            places_string += ', '.join([s[0]+', located at '+s[1] for s in shops])
        return 'The following places may have these books: '+places_string

    def process_find_library(self, text): # implement address queries
        text_l = text.lower()
        self.library_specifiers = re.findall(word_regex, text)
        self.current_processor = self.process_default
        if len(self.library_specifiers)==0:
            return 'Description is not clear'
        return self.answer_libraries_by_specifiers()

    def process_find_shop(self, text): # implement address queries
        text_l = text.lower()
        self.shop_specifiers = re.findall(word_regex, text)
        self.current_processor = self.process_default
        if len(self.shop_specifiers)==0:
            return 'Description is not clear'
        return self.answer_shops_by_specifiers()

    def search_book_by_name(self, name):
        if not self.database_connector:
            return None
        return self.database_connector.get_book(name)

    def search_books(self):
        if not self.database_connector:
            return None
        if len(self.current_authors)>0:
            books = self.database_connector.search_books_by_authors(self.current_authors)
        elif len(self.book_specifiers)>0:
            books = self.database_connector.search_books_by_genres(self.book_specifiers)
        else:
            books = []
        return books
        
    def search_libraries(self): # implement address queries
        if not self.database_connector:
            return None
        if len(self.library_specifiers)==0:
            return []
        return self.database_connector.get_libraries_by_specialties(self.library_specifiers)

    def search_shops(self): # implement address queries
        if not self.database_connector:
            return None
        if len(self.shop_specifiers)==0:
            return []
        return self.database_connector.get_shops_by_specialties(self.shop_specifiers)

    def search_libraries_by_books(self):
        if not self.database_connector:
            return None
        if len(self.current_books)==0:
            return []
        libraries = {(l[0],l[1]) for b in self.current_books for l in self.database_connector.search_libraries_with_book(b)}
        return list(libraries)

    def search_shops_by_books(self):
        if not self.database_connector:
            return None
        if len(self.current_books)==0:
            return []
        shops = {(s[0],s[1]) for b in self.current_books for s in self.database_connector.search_shops_with_book(b)}
        return list(shops)

    def get_all_genres(self):
        if not self.database_connector:
            return None
        return self.database_connector.get_genre_list()

    def get_all_specialties(self):
        if not self.database_connector:
            return None
        return self.database_connector.get_specialty_list()

    def __init__(self, database_connector):
        self.history = [] # tuples (text, time)
        self.current_processor = self.process_initial
        self.genre_desc = None
        self.library_specifiers = []
        self.shop_specifiers = []
        self.database_connector = database_connector
        self.current_books = []
        self.goodbye = False
        self.book_specifiers = []
        self.current_authors = []

    def process_user_text(self, text):
        self.history.append((text, datetime.datetime.now))
        result = self.current_processor(text)
        return result


if __name__=='__main__':
    DB_NAME = "postgres"
    USER = "postgres"
    PASSWORD = "postgres"
    HOST = "localhost"
    db = DatabaseConnector(DB_NAME, USER, PASSWORD, HOST)
    dialogue_processor = DialogueProcessor(db)
    while not dialogue_processor.goodbye:
        print(dialogue_processor.process_user_text(input()))
