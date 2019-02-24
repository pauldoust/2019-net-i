"""
DESCRIPTION
    Librarifier is a module used to create a Library file.
    
    The name of the newly generated file consists of the 'libr_' prefix,
    name of the file without extension, and '.libr' extension. For
    example, 'libr_hello.libr'.
    
    Library file itself is a JSON object which contains the following 
    key-value pairs (in arbitrary order):
        'hub_address': string, consists of IP:PORT combination
        'chunk_size': int, used to split file into pieces
        'hashes': array of hexadecimal hash strings of each piece
        'file_size': int, in bytes
        'file_name': string, includes actual name and extension

FUNCTIONS
    librarify(input_file, hub_address, chunk_size=2048, output_path=None)
        Generates a .libr description of input_file.

1 + 1 + 1 + 2 + 1 + 1 + 1
"""

import hashlib
import json
import math
import os.path
import socket
import unittest


# book (chunk) size, in bytes
from pathlib import Path

from app.utilites.netutils import Netutils

BOOK_SIZE = 2048
EXTENSION = '.lib'
PREFIX = 'lib_'


class Librarifier:
    # --- private functions ---
    def _bytes_to_sha1(chunk):
        """Returns a SHA1 hexadecimal hash string for a chunk of bytes."""

        hasher = hashlib.sha1()
        hasher.update(chunk)
        result = hasher.hexdigest()

        return result

    def _verify_input_file(input_file):
        """Raise errors if input_file is not a file or does not exist."""

        # raise TypeError if provided argument is not a string or bytestring
        file_type = type(input_file)
        if (file_type is not str) and (file_type is not bytes):
            raise TypeError('Provided input path is not string or bytes.')

        # raise ValueError if provided path is not a file
        if not os.path.isfile(input_file):
            raise ValueError('Provided input is not a file or does not exist.')

    def _verify_hub_address(hub_address):
        """Raise errors if argument is not a valid IPv4:PORT string."""

        # raise TypeError if provided argument is not a string
        if type(hub_address) is not str:
            raise TypeError('Provided hub address is not string or bytes.')

        # split on double-dot to get IP address part and port
        try:
            ip, port = hub_address.split(':')

            # check valid IPv4 address
            socket.inet_aton(ip)

            # check valid port
            is_port_in_range = (int(port) >= 0 and int(port) <= 65535)

            if not is_port_in_range:
                raise Exception('Port is invalid')

        except:
            raise ValueError('Provided hub address is invalid.')

    def _verify_output_path(output_path):
        """Raise errors if argument is not a string or not a valid path."""

        # raise TypeError if provided argument is not a string or bytestring
        type_path = type(output_path)
        if (type_path is not str) and (type_path is not bytes):
            raise TypeError('Provided output path is not a string.')

        # ValueError if path does not exist
        # raise ValueError if provided path is not a file
        if not os.path.exists(output_path):
            raise ValueError('Provided output path is not a valid path.')


    # --- public functions ---

    def librarify(input_file, hub_address, chunk_size=BOOK_SIZE, output_path=None):
        """Takes a file, generates a .libr library file and returns its path.

        Params:
        ------
        input_file -- a text or byte string giving the name of the file
            Should include the path if the file isn't in the
            current working directory.
        hub_address -- a string giving the address of the tracker and the port
            Should be in the following format: 'IPv4:PORT'.
            For example, '192.168.1.1:7777' is a valid hub address.
        chunk_size -- (int) size of each piece, in bytes.
            The input file will be split into chunks of the specified size.
        output_path -- (default None) is a path where libr file will be saved.
            If None, saves .libr in the same directory as input file.
        """

        # ERROR CHECKING AND HANDLING
        # make sure input_file exists
        Librarifier._verify_input_file(input_file)

        # make sure hub address is OK (right type, is actually an IP:port)
        Librarifier._verify_hub_address(hub_address)

        # make sure output_path is ok, if provided
        if output_path:
            Librarifier._verify_output_path(output_path)


        data = {'hub_address': hub_address, 'chunk_size': chunk_size}

        hashes = []
        with open(input_file, 'rb') as infile:

            while True:
                # read next chunk of bytes, quit if nothing left
                chunk_bytes = infile.read(chunk_size)

                if not chunk_bytes:
                    break

                # compute hash value of each book (chunk)
                chunk_hash = Librarifier._bytes_to_sha1(chunk_bytes)
                # save these values
                hashes.append(chunk_hash)

        data['hashes'] = hashes

        # get file size
        file_size = os.path.getsize(input_file)
        # make sure we correctly split the file in chunks
        assert( len(hashes) == math.ceil(file_size/chunk_size) )
        data['file_size'] = file_size

        # get filename with extension, save it, chop off extension
        input_file_directory, file_name = os.path.split(input_file)
        data['file_name'] = file_name
        pure_name, _ = os.path.splitext(file_name)

        # write meaningful information in library file
        if output_path is None:
            output_path = input_file_directory

        library_id = PREFIX + Netutils.get_timestamp()
        output_path = os.path.join(output_path,library_id + EXTENSION)

        with open(output_path, 'w') as outfile:
            json.dump(data, outfile,
                indent=4, sort_keys=True,
                separators=(',', ': '))

        # OUTPUT: the path to the newly created .libr file
        if Path(output_path).exists() :
            return True, library_id, output_path
        else:
            return False,library_id, output_path

# --- unit testing ---

class TestHashingFunction(unittest.TestCase):
    def test__bytes_to_sha1(self):
        self.assertEqual(
            Librarifier._bytes_to_sha1(b'hello'),
            'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d')

class TestVerificationFunctions(unittest.TestCase):

    def test__verify_input_file(self):
        with self.assertRaises(TypeError):
            Librarifier._verify_input_file(42)

        # check for incorrect path or non-existent file
        with self.assertRaises(ValueError):
            Librarifier._verify_input_file('abracadabra123')

    def test__verify_hub_address(self):
        # standard acceptance test
        self.assertEqual(Librarifier._verify_hub_address('192.168.1.1:7777'), None)
        
        # check for non-string input
        with self.assertRaises(TypeError):
            Librarifier._verify_hub_address(42)
        
        # check for gibberish
        with self.assertRaises(ValueError):
            Librarifier._verify_hub_address('abracadabra123')

        # check for incorrect IPv4
        with self.assertRaises(ValueError):
            Librarifier._verify_hub_address('1.1.2567.0:1234')

        # check for missing port
        with self.assertRaises(ValueError):
            Librarifier._verify_hub_address('192.168.1.1')

        with self.assertRaises(ValueError):
            Librarifier._verify_hub_address('192.168.1.1:')

        # check for port out of bounds
        with self.assertRaises(ValueError):
            Librarifier._verify_hub_address('192.168.1.1:90000')

        with self.assertRaises(ValueError):
            Librarifier._verify_hub_address('192.168.1.1:-1')

    def test__verify_output_path(self):

        # check for non-string input
        with self.assertRaises(TypeError):
            Librarifier._verify_output_path(42)

        # check for incorrect path or non-existent file
        with self.assertRaises(ValueError):
            Librarifier._verify_input_file('abracadabra123')


if __name__ == '__main__':
    unittest.main()

# testing the module
    # informal code inspection
    
    # unit tests
        # different files (mp3, jpeg, txt, py, etc.)
        # invalid user input
        # correctness of hashing
