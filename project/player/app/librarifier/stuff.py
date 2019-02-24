from  app.librarifier.book import Book
from app.settings.config import  Config
import pickle
import os

class Stuff:

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            # print(type(bytearray(data)))
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
                    # print(book.getSize())
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
            # print(type(book.book_bytes))
            data  = data + book.book_bytes
        print("final: ", len(data))
        self.create_file(filePath, data)

    def create_file(self, filePath, data):
        print("Writing to file")
        with open(filePath, 'wb') as file:
            file.write(data)
        return True


    def is_download_complete(self):
        print("number_of_books_received", str(len(self.list_book_received)) )
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
    read_file_path = Config.MYDB_DIR +os.sep+ "images.jpeg"
    write_stuff_file_path = Config.STUFFS_DIR +os.sep+"data.pkl"
    write_full_file_path = Config.DOWNLOAD_DIR +os.sep+ "images_downloaded.jpg"

    #persist
    s = Stuff(read_file_path, 1024)
    print(s.total_no_books)
    s.persist(write_stuff_file_path)


    #load
    s = Stuff.load(write_stuff_file_path)
    print(s.total_no_books)
    s.flushToFile(write_full_file_path)
    # Flashing  should be progressive