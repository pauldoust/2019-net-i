from collections import Counter
from itertools import chain
from queue import PriorityQueue

from  app.librarifier.book import Book
from app.settings.config import  Config
import pickle
import os

from app.utilites.auxiliaries import Auxiliaries


class Stuff:

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            # Auxiliaries.console_log(type(bytearray(data)))
            if not data:
                break
            yield data

    def __init__(self, file_path = None, chunk_size =1024 , total_no_books = 0):
        self.books = []
        self.total_no_books = total_no_books
        self.list_book_received = set()

        if file_path is not None:
            with open(file_path, 'rb') as file:
                book_id= 0
                for piece in self.read_in_chunks(file, chunk_size):
                    self.total_no_books += 1
                    if book_id not in self.list_book_received:
                        self.list_book_received.add(book_id)
                        book_id += 1
                    book = Book()
                    book.book_bytes = bytearray(piece)
                    # Auxiliaries.console_log(book.getSize())
                    self.books.append(book)
                    # self.books = [Book(piece) for i in range(books_num)]


    def createSeedBooks(self, no_books ):
        self.total_no_books = no_books
        for i in range(0, no_books):
            self.books.append(Book())


    def storeBook(self, book, book_id ):
        self.books[book_id].book_bytes = book
        if book_id not in  self.list_book_received:
            self.list_book_received.add(book_id)

    def fetchBook(self, book_id):
        return self.books[book_id]

    def flushToFile(self, filePath):
        data = bytearray()
        for book in self.books:
            # Auxiliaries.console_log(type(book.book_bytes))
            data  = data + book.book_bytes
        Auxiliaries.console_log("final: ", len(data))
        self.create_file(filePath, data)

    def create_file(self, filePath, data):
        Auxiliaries.console_log("Writing to file")
        with open(filePath, 'wb') as file:
            file.write(data)
        return True

    def getPriorityBooks(self, availableBooks):
        q = PriorityQueue()
        data = list(chain.from_iterable(availableBooks))
        dictPriorityBooks = dict(Counter(data))
        print("counts", dictPriorityBooks)
        for key, value in dictPriorityBooks.items():
            q.put((value, key))

        while not q.empty():
            next_item = q.get()
            print(next_item)
        return q


    def is_download_complete(self):
        Auxiliaries.console_log("number_of_books_received", str(len(self.list_book_received)) )
        if len(self.list_book_received) == self.total_no_books:
            return True
        return  False

    def persist(self, dumpPath):
        output = open(dumpPath, 'wb')
        pickle.dump(self, output)
        output.close()

    @staticmethod
    def load(pkl_path):
        pkl_file = open(pkl_path, 'rb')
        obj = pickle.load(pkl_file)
        pkl_file.close()
        return obj

    def get_list_book_received(self):
        return self.list_book_received




if __name__ == "__main__":
    """
    read_file_path = Config.MYDB_DIR +os.sep+ "images.jpeg"
    write_stuff_file_path = Config.STUFFS_DIR +os.sep+"data.pkl"
    write_full_file_path = Config.DOWNLOAD_DIR +os.sep+ "images_downloaded.jpg"

    #persist
    s = Stuff(read_file_path, 1024)
    Auxiliaries.console_log(s.total_no_books)
    s.persist(write_stuff_file_path)


    #load
    s = Stuff.load(write_stuff_file_path)
    Auxiliaries.console_log(s.total_no_books)
    s.flushToFile(write_full_file_path)
    # Flashing  should be progressive
    """

    # test Priority Queue
    my_list = [[1, 2, 3], [4, 3, 2, 1, 5, 6], [1, 2, 3, 7, 8, 9, 10], [11, 12, 1, 14, 3, 1, 5, 6], [1], [3]]
    # persist
    s = Stuff("/media/betek/LENOVO/solve_ai.mp3", 1024)
    print(s.getPriorityBooks(my_list))