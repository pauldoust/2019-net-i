# Librarifier

Librarifier is a small sub-module used to create a **.libr** meta-file.

Given a path ot the original file, creates **a text file with JSON object**, which encodes 
**a dictionary** with the following key-value pairs (in arbitrary order):

* *'hub_address': string*, consists of IP:PORT combination
* *'chunk_size': integer*, used to split original file into pieces
* *'hashes': array* of hexadecimal hash strings of each piece
* *'file_size': integer*, in bytes
* *'file_name': string*, includes actual name and extension
