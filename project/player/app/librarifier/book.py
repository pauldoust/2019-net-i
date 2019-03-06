class Book:
    def __init__(self, book_bytes):
        # self.book_bytes =  bytearray()
        self.book_bytes = book_bytes

    def __init__(self):
        self.book_bytes =  bytearray()

    def getSize(self):
        return len(self.book_bytes)

