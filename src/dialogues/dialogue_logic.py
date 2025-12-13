# code written here will be responsible for answering users input
import os
from enum import Enum
import datetime
from dialogues.text_processing import *
import re
from database.database import DatabaseConnector

class Emotion(Enum):
    IDLE = 0
    THINK = 1
    WAIT = 2
    TALK = 4
    TELL = 5
    YES = 6
    NO = 7
    ASK = 8

EmotionString = {Emotion.IDLE:'Idle',
                 Emotion.THINK:'Think',
                 Emotion.WAIT:'Wait',
                 Emotion.TALK:'Talk',
                 Emotion.TELL:'Tell',
                 Emotion.YES:'Yes',
                 Emotion.NO:'No',
                 Emotion.ASK:'Ask'}

class DialogueProcessor:
    def format_as_dict(self, text=None, emotion=None, table_header=None, table_body=None):
        return {'text':text, 'emotion':EmotionString[emotion] if emotion in EmotionString else EmotionString[Emotion.TALK], 'table_header':table_header, 'table_body':table_body}

    def process_initial(self, text):
        text_l = text.lower()
        words = re.findall(word_regex, text_l)
        default_reply = 'Hello, how can I assist you? Say help for a quick tutorial. If you have problems with speech input, check a checkbox to switch to text'
        default_table_h = ['Basic dialogue options']
        default_table_b = [['Find [genres] book [authored by] [name is]'],
                           ['Find library'],
                           ['Find shop'],
                           ['List genres'],
                           ['List specialties'],
                           ['... and so on']]
        if not self.database_connector:
            default_reply += ' Unfortunately my database is not connected, so I have limited knowledge'
        if len(words)==0:
            return self.format_as_dict(default_reply, Emotion.TALK, default_table_h, default_table_b)
        hello_detected = False
        for w in hello_words:
            if w in words:
                if len(words) == 1:
                    return self.format_as_dict(default_reply, Emotion.TALK, default_table_h, default_table_b)
                hello_detected = True
                break
        # add more hello extensions later
        return self.process_default(text)
        
    def process_default(self, text):
        text_l = text.lower()
        if re.match('goodbye.*', text_l):
            self.goodbye = True
            return self.format_as_dict('Goodbye', Emotion.TELL)
        elif book_desc:=re.search(r'(?:\bfind\b|\bsearch\s+for\b)(.*)(?:book)(.*)', text_l):
            self.book_specifiers = re.findall(word_regex, book_desc.group(1))
            book_description = book_desc.group(2)
            self.current_authors = []
            if authored := re.search(r'(?:\bauthored\s+by\b|\bwith\b.*\bauthors)(.*)', book_description):
                potential_authors = [s for s in re.findall(word_regex, authored.group(1)) if s!='and']
                if len(potential_authors)==0:
                    self.current_processor = self.process_clarify_authors
                    return self.format_as_dict('Please clarify authors or say cancel to stop', Emotion.ASK)
                else:
                    return self.answer_for_nonempty_potential_authors(potential_authors)
            elif len(self.book_specifiers)>0:
                return self.answer_books_by_genres_only()
            else:
                self.current_processor = self.process_find_book
                return self.format_as_dict('Please describe the book you want to find', Emotion.ASK)
        elif library_desc:=re.search(r'(?:\bfind\b|\bsearch\b(?:\s+for\b)?)(.*)(?:librar(?:y|ies))(.*)', text_l):
            self.library_specifiers = [s for s in re.findall(word_regex, library_desc.group(1)) if s!='and']
            if close_to:=re.search(r'(?:\bnear\b|\bclose\b(?:\s+to\b)?)(.*)', library_desc.group(2)):
                if re.search(r'(?:\bme\b|(?:\bmy\b(?:home|house|location)))', close_to.group(1)):
                    return self.format_as_dict('Address queries are not implemented yet') # implement
                else:
                    return self.format_as_dict('Address queries are not implemented yet') # implement
            elif place_desc := re.search(r'(?:\bin\b)(.*)', library_desc.group(2)):
                if re.search(r'(?:\bmy\s+(?:town|city))', place_desc.group(1)):
                    return self.format_as_dict('Address queries are not implemented yet') # implement
                else:
                    return self.format_as_dict('Address queries are not implemented yet') # implement
            else:
                if len(self.library_specifiers)==0:
                    self.current_processor = self.process_find_library
                    return self.format_as_dict('Describe the library you want to find', Emotion.ASK)
                else:
                    return self.answer_libraries_by_specifiers()
        elif shop_desc:=re.search(r'(?:\bfind\b|\bsearch\b(?:\s+for\b)?)(.*)(?:shops?)(.*)', text_l):
            self.shop_specifiers = [s for s in re.findall(word_regex, shop_desc.group(1)) if s!='and']
            if close_to:=re.search(r'(?:\bnear\b|\bclose\b(?:\s+to\b)?)(.*)', shop_desc.group(2)):
                if re.search(r'(?:\bme\b|(?:\bmy\b(?:home|house|location)))', close_to.group(1)):
                    return self.format_as_dict('Address queries are not implemented yet') # implement
                else:
                    return self.format_as_dict('Address queries are not implemented yet') # implement
            elif place_desc := re.search(r'(?:\bin\b)(.*)', shop_desc.group(2)):
                if re.search(r'(?:\bmy\s+(?:town|city))', place_desc.group(1)):
                    return self.format_as_dict('Address queries are not implemented yet') # implement
                else:
                    return self.format_as_dict('Address queries are not implemented yet') # implement
            else:
                if len(self.shop_specifiers)==0:
                    self.current_processor = self.process_find_shop
                    return self.format_as_dict('Describe the shop you want to find', Emotion.ASK)
                else:
                    return self.answer_shops_by_specifiers()
        elif re.search(r'\b(list|get|describe|tell)\b.*\bgenre', text_l):
            genres = self.get_all_genres()
            if not genres:
                return self.format_as_dict('Database connection issues, sorry', Emotion.NO)
            return self.format_as_dict('The following genres are present in my database: '+', '.join(genres[:self.max_told_items])+('and so on' if len(genres)>self.max_told_items else ''), Emotion.TELL, ['Genre'], [[g] for g in genres])
        elif re.search(r'\b(list|get|describe|tell)\b.*\bspecialt', text_l):
            specialties = self.get_all_specialties()
            if not specialties:
                return self.format_as_dict('Database connection issues, sorry', Emotion.NO)
            return self.format_as_dict('The following library and shop specialties are present in my database: '+', '.join(specialties[:self.max_told_items])+('and so on' if len(specialties)>self.max_told_items else ''), Emotion.TELL, ['Specialty'], [[s] for s in specialties])

        return self.format_as_dict('Hello, your request was not recognised. If you need help, say help.', Emotion.NO)

    def process_clarify_authors(self, text):
        text_l = text.lower()
        if re.match(r'cancel\b', text_l):
            self.current_processor = self.process_default
            return self.format_as_dict('Cancelled', Emotion.YES)
        potential_authors = [s for s in re.findall(word_regex, text_l) if s!='and']
        if len(potential_authors)==0:
            return self.format_as_dict('Input unclear again, please repeat authors or cancel search', Emotion.ASK)
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
            return self.format_as_dict('Seems like no books from this author is in database', Emotion.NO)
        else:
            self.current_processor = self.process_after_book_found
            self.current_books = books
            return self.format_as_dict('The following books were found: '+', '.join(books[:self.max_told_items]) +('and so on' if len(books)>self.max_told_items else '')+ '. Do you want me to search for them in libraries or shops?', Emotion.WAIT, ['Book'], [[b] for b in books])

    def answer_books_by_genres_only(self):
        books = self.search_books()
        if not books:
            return self.format_as_dict('There are problems with database connection', Emotion.NO)
        if len(books) == 0:
            self.current_processor = self.process_default
            return self.format_as_dict('Seems like there are no books corresponding to the description', Emotion.NO)
        self.current_books = books
        self.current_processor = self.process_after_book_found
        return self.format_as_dict('The following books were found: ' + ', '.join(books[:self.max_told_items]) + ('and so on' if len(books)>self.max_told_items else '') + '. Do you want me to serach for them in librarier or shops?', Emotion.WAIT, ['Book'], [[b] for b in books])

    def answer_book_name(self, name, none_if_negative = False):
        book = self.search_book_by_name(name)
        if not book:
            if none_if_negative:
                return None
            else:
                self.current_processor = self.process_default
                return self.format_as_dict('Book with this name was not found')
        self.current_processor = self.process_after_book_found
        self.current_books = book
        return self.format_as_dict('There is a book with name '+book[0]+' written by '+', '.join(book[1])+'. Want me to search it in shops or libraries?', Emotion.WAIT, ['Name', 'Authors', 'Genres'], [[book[0], ', '.join(book[1]), ', '.join(book[2])]])

    def answer_libraries_by_specifiers(self):
        libraries = self.search_libraries()
        self.current_processor = self.process_default
        if len(libraries)==0:
            return self.format_as_dict('No libraries with specified description found')
        return self.format_as_dict('Libraries corresponding to description: '+', '.join([l[0] for l in libraries[:self.max_told_items]]), Emotion.TELL, ['Name', 'Location'], [[l[0], l[1]] for l in libraries])

    def answer_shops_by_specifiers(self):
        shops = self.search_shops()
        self.current_processor = self.process_default
        if len(shops)==0:
            return self.format_as_dict('No shops with specified description found')
        return self.format_as_dict('Shops corresponding to description: '+', '.join([s[0] for s in shops[:self.max_told_items]]), Emotion.TELL, ['Name', 'Location'], [[s[0], s[1]] for s in shops])

    def process_find_book(self, text):
        text_l = text.lower()
        if text_l == 'cancel':
            self.current_processor = self.process_default
            return self.format_as_dict('Cancelling search', Emotion.YES)
        if book_name:=re.search(r'(?:\bname\b).*(?:\bis\b)?(.*)', text_l):
            name = book_name.group(1)
            return self.answer_book_name(name)
        if authors_desc:=re.search(r'(?:authors?)(?:.*is|.*are)?(.*)', text_l):
            potential_authors = [s for s in re.findall(word_regex, authors_desc.group(1)) if s!='and']
            if len(potential_authors)==0:
                self.current_processor = self.process_clarify_authors
                return self.format_as_dict('Could not understand authors, please repeat or say cancel to stop', Emotion.ASK)
            else:
                return self.answer_for_nonempty_potential_authors(potential_authors)
        elif genre_desc:=re.search(r'(?:genres?)(?:.*is|.*are)?(.*)', text_l):
            self.book_specifiers = re.findall(word_regex, genre_desc.group(1))
            if len(self.book_specifiers)>0:
                return self.answer_books_by_genres_only()
        return self.format_as_dict('Description is not recognisable, please say book genres, name or authors, or say cancel if you want to stop', Emotion.WAIT)

    def process_after_book_found(self, text):
        text_l = text.lower()
        places_string = ''
        in_libraries = text_l == 'yes' or re.search(r'\blibrar', text_l)
        in_shops = text_l == 'yes' or re.search(r'\bshop', text_l)
        self.current_processor = self.process_default
        if not in_libraries and not in_shops:
            if text == 'no':
                return self.format_as_dict('Stopping search', Emotion.YES)
            else:
                return self.format_as_dict('Request not recognised', Emotion.NO)
        num_told = 0
        places = []
        if in_libraries:
            libraries = self.search_libraries_by_books()
            num_told += len(libraries)
            places_string += ', '.join([l[1] for l in libraries[:self.max_told_items]])
            places += [[l[0], l[1], l[2], 'yes' if l[3] else 'no', l[4] if l[4] else ''] for l in libraries]
        if in_shops and num_told<self.max_told_items:
            shops = self.search_shops_by_books()
            places_string += ', '.join([s[1] for s in shops[:self.max_told_items-num_told]])
            places += [[s[0], s[1], s[2], s[3], s[4] if s[4] else ''] for s in shops]
        return self.format_as_dict('The following places may have these books: '+places_string, Emotion.TELL, ['Book', 'Place', 'Location', ('Price/Available' if in_shops else 'Availability') if in_libraries else 'Price', 'Link'], places)

    def process_find_library(self, text): # implement address queries
        text_l = text.lower()
        self.library_specifiers = re.findall(word_regex, text)
        self.current_processor = self.process_default
        if len(self.library_specifiers)==0:
            return self.format_as_dict('Description is not clear', Emotion.NO)
        return self.answer_libraries_by_specifiers()

    def process_find_shop(self, text): # implement address queries
        text_l = text.lower()
        self.shop_specifiers = re.findall(word_regex, text)
        self.current_processor = self.process_default
        if len(self.shop_specifiers)==0:
            return self.format_as_dict('Description is not clear', Emotion.NO)
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
        libraries = {(b,l[0],l[1],l[2],l[3]) for b in self.current_books for l in self.database_connector.search_libraries_with_book(b)}
        return list(libraries)

    def search_shops_by_books(self):
        if not self.database_connector:
            return None
        if len(self.current_books)==0:
            return []
        shops = {(b,s[0],s[1],s[2],s[3]) for b in self.current_books for s in self.database_connector.search_shops_with_book(b)}
        return list(shops)

    def get_all_genres(self):
        if not self.database_connector:
            return None
        return self.database_connector.get_genre_list()

    def get_all_specialties(self):
        if not self.database_connector:
            return None
        return self.database_connector.get_specialty_list()

    def __init__(self, database_connector: DatabaseConnector, max_told_items = 5):
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
        self.max_told_items = max_told_items

    def process_user_text(self, text):
        self.history.append((text, datetime.datetime.now))
        result = self.current_processor(text)
        return result


if __name__=='__main__':
    DB_NAME = "postgres"
    USER = "postgres"
    PASSWORD = os.getenv("POSTGRES_PASS", "postgres")
    HOST = "localhost"
    db = DatabaseConnector(DB_NAME, USER, PASSWORD, HOST)
    dialogue_processor = DialogueProcessor(db)
    while not dialogue_processor.goodbye:
        print(dialogue_processor.process_user_text(input()))
