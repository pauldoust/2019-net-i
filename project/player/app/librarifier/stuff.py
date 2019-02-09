from book import *
import pickle
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

    def __init__(self):
        # self.id= ...
        self.books = []
        # self.books = [Book() for i in range(books_num)]

    def __init__(self, file_path, chunk_size):
        self.books = []
        with open(file_path, 'rb') as file:
            for piece in self.read_in_chunks(file, chunk_size):
                book = Book()
                book.book_bytes = bytearray(piece)
                # print(book.getSize())
                self.books.append(book)
                # self.books = [Book(piece) for i in range(books_num)]

    def storeBook(self, book, book_id ):
        self.books[book_id].book_bytes = book

    def fetchBook(book_id):
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



    def persist(self, dumpPath):
        output = open('data.pkl', 'wb')
        pickle.dump(self, output)
        output.close()

    @staticmethod
    def load(pkl_path):
        pkl_file = open(pkl_path, 'rb')
        obj = pickle.load(pkl_file)
        pkl_file.close()
        return obj







read_file_path = r'D:\test.mp4'
write_file_path = r'D:\test2.mp4'

#persist
# s = Stuff(read_file_path, 1024)
# s.persist('data.pkl')


#load
s = Stuff.load('data.pkl')
s.flushToFile(write_file_path)