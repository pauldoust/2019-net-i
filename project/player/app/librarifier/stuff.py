from book import *
import pickle
import pandas as pd
from collections import Counter
from itertools import chain
from queue import PriorityQueue

class Stuff:

	def read_in_chunks(self, file_object, chunk_size=1024):
		while True:
			data = file_object.read(chunk_size)
			if not data:
				break
			yield data

	def __init__(self, file_path = None, chunk_size = None):
		self.books = {}
		if file_path is None:
			return
		bookIndex = 0
		with open(file_path, 'rb') as file:
			for piece in self.read_in_chunks(file, chunk_size):
				book = Book()
				book.book_bytes = bytearray(piece)
				self.storeBook(book, bookIndex)
				bookIndex = bookIndex +1
				if bookIndex == 100:
					return
	def storeBook(self, book, book_id ):
		self.books[book_id] = book


	def getNeededBooks(self):
		return len(self.books)

	def getPriorityBooks(self, availableBooks):
		q = PriorityQueue()
		data = list(chain.from_iterable(availableBooks))
		dictPriorityBooks = dict(Counter(data))
		print("counts" , dictPriorityBooks)
		for key,value in dictPriorityBooks.items():
			q.put((-value,key))
		# while not q.empty():
 	# 	   next_item = q.get()
 	# 	   print(next_item)
 		return q


	def fetchBook(book_id):
		return self.books[book_id]

	def flushToFile(self, filePath):
		data = bytearray()
		for bookIndex in self.books:
			book = self.books[bookIndex]
			# print(type(book.book_bytes))
			print("booky", book)
			data  = data + book.book_bytes
		print("final: ", le(ndata))
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
write_file_path = r'D:\test234.mp4'


my_list=[[1,2, 3],[4, 3 ,2 ,1 ,5, 6],[1, 2, 3, 7, 8, 9, 10],[11, 12, 1, 14 , 3 ,1 , 5 ,6],[1],[3]]
#persist
s = Stuff(read_file_path, 1024)
s.getPriorityBooks(my_list)
# print(s.getNeededBooks())
# s.persist('data.pkl')


#load
# s = Stuff.load('data.pkl')
# s.flushToFile(write_file_path)