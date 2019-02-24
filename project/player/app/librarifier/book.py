class Book:
    def __init__(self, book_bytes = None):
        self.book_bytes =  bytearray()
        if book_bytes is not None:
            self.book_bytes = book_bytes



    def getSize(self):
        return len(self.book_bytes)

