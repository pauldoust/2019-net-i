import pickle
import traceback
from itertools import chain
from queue import PriorityQueue
from collections import Counter
from app.librarifier.book import Book
from app.utilites.auxiliaries import Auxiliaries
from random import randrange

class Stuff:

    def read_in_chunks(self, file_object, chunk_size=1024):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data


    def getProgress(self):
        Auxiliaries.console_log ("received so far:  ", len(self.list_book_received), " / ", self.total_no_books)
        # print ("received so far:  ", len(self.list_book_received), " / ", self.total_no_books)

        return len(self.list_book_received ) / self.total_no_books



    def __init__(self, file_path = None, chunk_size = 1024,  total_no_books = 0):
        self.availableBooks = dict()
        # self.lock = threading.Lock()
        self.books = {}
        self.total_no_books = total_no_books
        self.list_book_received = set()

        if file_path is None:
            return

        bookIndex = 0
        with open(file_path, 'rb') as file:
            for piece in self.read_in_chunks(file, chunk_size):
                book = Book()
                book.book_bytes = bytearray(piece)
                self.storeBook(book, bookIndex)
                bookIndex = bookIndex +1
            if self.total_no_books == 0:
                self.total_no_books = bookIndex

    def storeBook(self, book, book_id ):
        self.books[book_id] = book
        # print(type(self.books))
        # print(type(book_id))
        if book_id not in  self.get_list_book_received():
            self.list_book_received.add(book_id)

    def constructBook(self, b_bytes, book_id ):
        try:
            # print("type: ", type(book))
            book = Book()
            book.book_bytes = bytearray(b_bytes)
            self.storeBook(book, book_id)
        except Exception as e :
            Auxiliaries.console_log("Exception", e)
            traceback.printnt_exc()
            # sys.exit(1)
    
    def fetchBook(self, book_id):
        return self.books[book_id]

    def getNeededBooks(self):
        return len(self.books)

    def getPriorityBooks(self, availableBooks):
        q = PriorityQueue()
        data = list(chain.from_iterable(availableBooks))
        dictPriorityBooks = dict(Counter(data))
        # print("counts" , dictPriorityBooks)
        for key, value in dictPriorityBooks.items():
            q.put((-value, key))
        return q

    def flushToFile(self, filePath):
        data = bytearray()
        # print(type(self.books))
        index = 0
        for bookIndex in self.books:
            book = self.books[index]
            index = index + 1
            # print(bookIndex)
            # print(type(book))
            data  = data + book.book_bytes
        Auxiliaries.console_log("final: ", len(data))
        self.create_file(filePath, data)

    def create_file(self, filePath, data):
        Auxiliaries.console_log("Writing to file")
        with open(filePath, 'wb') as file:
            file.write(data)
        return True

    def is_download_complete(self):
        if len(self.list_book_received) == self.total_no_books:
            return True
        return  False

    def persist(self, dumpPath):
        output = open(dumpPath, 'wb')
        pickle.dump(self, output)
        output.close()

    def get_list_book_received(self):
        return self.list_book_received

    def getPriorityBooks(self, availableBooks):
        # print(availableBooks)
        q = PriorityQueue()
        data = list(chain.from_iterable(availableBooks))
        dictPriorityBooks = dict(Counter(data))
        # print("counts" , dictPriorityBooks)
        for key,value in dictPriorityBooks.items():
            ourKey =   str(randrange(1,1000)) + ":" + str(key) 
            q.put((value,ourKey))
        # while not q.empty():
        #  next_item = q.get()
        #  print(next_item[0], next_item[1])
        return q

    def storeAvailableBooks(self, peerId, availableBooks ):
        # self.lock.acquire()
        try: 
            # print("storeBook: ", peerId , " - ", availableBooks )
            self.availableBooks[peerId] = availableBooks

        except Exception as e:
            Auxiliaries.console_log("Exception in storeAvailableBooks: {} ".format(e))
        # finally:  
            # self.lock.release()

    def getNextBook(self, peerId, collected_books):
        # self.lock.acquire()
        try: 
            # print("started")
            collected = [ x[0] for x in collected_books]
            allBooksList = []
            for key, value in self.availableBooks.items():
                allBooksList.append(value)
            # print("all Books: ", allBooksList)

            pq = self.getPriorityBooks(allBooksList)
            # print('queue: ', pq.queue)
            # while not pq.empty():
            #     next_item = pq.get()
            #     freq = next_item [0]
            #     element = next_item[1]
            #     element = element.split(":") [1]
            #     print(freq, element)

            # return
            while not pq.empty():
                 next_item = pq.get()[1]
                 next_item = next_item.split(":")[1]
                 next_item = int(next_item)
                 # print('next_item: ', next_item)
                 if next_item in self.availableBooks[peerId]:
                    # print("in", self.get_list_book_received())
                    if next_item not in  self.get_list_book_received() and next_item not in collected:
                        # print("returning: ", next_item)
                        return next_item

            # print("end")
            return None
        except Exception as e:
            Auxiliaries.console_log("Exception in getNextBook: {} ".format(e))
        # finally:
            # self.lock.release()

    @staticmethod
    def load(pkl_path):
        pkl_file = open(pkl_path, 'rb')
        obj = pickle.load(pkl_file)
        pkl_file.close()
        return obj

