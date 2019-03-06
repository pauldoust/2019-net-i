"""
To bring hub on-line, just run this. To connect, peers must know your IP
and PORT.

DESCRIPTION
    hub module keeps track of available peers and handles their requests.

    The hub maintains a database to keep track of libraries and corresponding 
    lists of peers. On a boot up, hub tries to recover previously saved
    database; otherwise, it initializes empty one.
    
    While running, it accepts a connection and allocates a thread to deal with
    further communication. Once connection is accepted, hub tries to receive 
    a message from a client, decode it into a request and then execute 
    the request.

    If the request is invalid (valid command, bad arguments, etc.), closes the 
    client socket connection, sends back error code and stops the allocated 
    thread.

    Once in a while the hub makes a backup of its current database.

1 + 1 + 1 + 1 + 1 + 1 + 1 + 2
"""

import _thread
import json
import socket
import time

from config import *  # import global constants
from database import Database
from threading import Timer


# allocate locks for database ADT and printing
DATABASE_LOCK = _thread.allocate_lock()
PRINT_LOCK = _thread.allocate_lock()


# --- client thread function ---
def _handle_client(client_socket):
    """Receives and handles client's request, then closes the socket.

    Function reads data from client_socket, decodes to get the request. 
    Based on the request, calls necessary procedure to execute it. 
    Then, closes the connection.

    If exception is raised in any of the methods called from here, it
    catches exception, sends back the error code, closes the socket 
    and re-raises exception to exit the thread.

    Params:
    ---
    client_socket -- alive socket connection with the client
        Client is expected to send the request, otherwise he times out.
    """
    
    # read data from TCP socket (binary stream)
    try:
        data = _read_data(client_socket)
    # close, send code and raise error if timed out or message is too big
    except (MemoryError, TimeoutError):
        # TODO: warn log
        client_socket.sendall(b_SERVER_ERROR + MESSAGE_END)
        client_socket.close()
        raise

    # decode the message into (hopefully) a request string
    data = data.decode(CODEC)

    with PRINT_LOCK:
        print('Message acquired:', data)

    # based on the data string, try to resolve the request
    try:
        _resolve(request=data, client_socket=client_socket)
    # TODO: warn? log
    except InvalidCommandError:
        client_socket.sendall(b_INVALID_COMMAND + MESSAGE_END)
        client_socket.close()
        raise
    except InvalidArgumentsError:
        client_socket.sendall(b_INVALID_ARGUMENTS + MESSAGE_END)
        client_socket.close()
        raise
    except InvalidSyntaxError:
        client_socket.sendall(b_INVALID_SYNTAX + MESSAGE_END)
        client_socket.close()
        raise

    # gracefully close the connection
    client_socket.close()


# --- helper functions ---
def _read_data(client_socket):
    """Reads from sock until delimiter and returns a binary string received.

    Reads byte by byte from client_socket until MESSAGE_END is seen.

    Raises MemoryError if message is too long. Raises TimeoutError 
    if client socket times out after TIMEOUT seconds.

    Returns:
    ---
    data -- binary string
    """

    # set time out
    client_socket.settimeout(TIMEOUT)

    # read stream byte by byte until next encountered sign is MESSAGE_END
    is_flag_received = False

    # to aggregate the byte stream
    data = []

    # read from socket into data
    while True:
        # --- try getting next byte ---
        try:
            byte_received = client_socket.recv(1)
        except socket.timeout:
            raise TimeoutError('Client connection timed out.')
    
        # --- check end message ---
        if byte_received == BEFORE_END_FLAG:
            is_flag_received = True

        elif (byte_received == END_SYMBOL) and is_flag_received == True:
            break

        # --- append the byte to the data ---
        else:
            data.append(byte_received)

            # re-set the flag
            is_flag_received = False

            # check message length
            if len(data) >= MAX_MESSAGE_LENGTH:
                raise MemoryError('Received message is too big.')

    # arrange the data in one binary string to reconstruct original message
    data = b''.join(data)

    return data

# --- control point - decides what to do based upon the request ---
def _resolve(request, client_socket):
    """Based on the request, calls other functions to satisfy it.
    
    Given a REGISTER_PEER request, registers a peer. Given a LIST_PEERS
    request, sends back a list of peers. Given DELETE request, deletes
    a specified library.

    Raises InvalidCommandError if request is not recognized.
    
    Params:
    ---
    request -- raw string with (hopefully) correct request
    client_socket -- open socket connection with the client
        Is used to send back the codes and data.
    """

    # split the request
    splitted_request = request.split(' ')

    # get the first COMMAND word
    request_to_check = str(splitted_request[0]).lower()

    # call needed routine
    if request_to_check == 'register_peer':
        _register_peer(request, client_socket)
        
    elif request_to_check == 'list_peers':
        _list_peers(request, client_socket)

    elif request_to_check == 'delete':
        _delete(request, client_socket)

    # if the word does not correspond to known COMMAND, raise error
    else:
        raise InvalidCommandError('Invalid request.')

# --- actual request calls ---
def _register_peer(request, client_socket):
    """Adds a peer to the database.
    
    Given a REGISTER_PEER request, acquires DATABASE_LOCK and adds a 
    peer to the DATABASE. On success, sends code back using client_socket.

    Raises ValueError if request format is invalid.
    
    Params:
    ---
    request -- string of form 'REGISTER_PEER {library} {IPv4} {port}'
    client_socket -- alive socket connection with the client   
    """

    # TODO: make sure request is correct
    # parse the request
    try:
        _, library_id, peer_ip, peer_port = request.split(' ')
    except:
        raise InvalidSyntaxError('Invalid request syntax.')

    # TODO: check the correctness of peer ipv4+port combo
    # TODO: check correctness of library_id

    # get peer ip+port, create a peer tuple object
    peer_id = (str(peer_ip), str(peer_port))

    # TODO: better databases interaction - initialize empty array in dict
    # TODO: adding duplicate peer_ids
    
    # with lock, add the peer to correct library (create new one if necessary)
    global DATABASE, DATABASE_LOCK
    with DATABASE_LOCK:
        DATABASE.add_peer(peer_id, library_id)

    with PRINT_LOCK:
        print('Added the peer', peer_id, 'to', library_id)
    # TODO: info log

    # return the 'OK' response to the peer using client_socket
    client_socket.sendall(b_OK + MESSAGE_END)

def _list_peers(request, client_socket):
    """Sends json-encoded list of peers through the client_socket.
    
    Given a LIST_PEERS request, acquires DATABASE_LOCK, samples
    PEER_COUNT peers from DATABASE, serializes the list into the json
    string and sends it back using client_socket.

    Raises ValueError if request format is invalid.
    
    Params:
    ---
    request -- string of form 'LIST_PEERS {library}'
    client_socket -- open socket connection with the client   
    """

    # get the library id/name
    splitted_request = request.split()
    try:
        library_id = splitted_request[1]
    except:
        raise InvalidSyntaxError('Request format is invalid')

    # with the lock,
    # get the subset of peer ip+port items from our database
    global DATABASE, DATABASE_LOCK
    with DATABASE_LOCK:
        sampled_peers = DATABASE.list_peers(library_id, PEER_COUNT)

    with PRINT_LOCK:
        print('List of sampled peers:', sampled_peers)
    # TODO: info log

    # put it in json string
    json_result = json.dumps(
        sampled_peers,
        sort_keys=True,
        separators=(',', ': ')
        )
    
    # construct the response
    # TODO: add one more field with number of peers (see protocol)
    response = b_OK + b' ' + json_result.encode(CODEC) + MESSAGE_END

    with PRINT_LOCK:
        print('The message:', response)
    
    # send the response to the client
    client_socket.sendall(response)

def _delete(request, client_socket):
    """Deletes a library from the database."""

    try:
        _, library_id = request.split(' ')
    except:
        raise InvalidSyntaxError('Invalid request syntax.')

    global DATABASE, DATABASE_LOCK
    with DATABASE_LOCK:
        DATABASE.drop(library_id)

    with PRINT_LOCK:
        print('Dropped the library', library_id)
    # TODO: info log

    # return the 'OK' response to the peer using client_socket
    client_socket.sendall(b_OK + MESSAGE_END)


# --- persistence procedure ---
def _save_database():
    """With lock, saves the database."""

    global DATABASE, DATABASE_LOCK

    with DATABASE_LOCK:
        DATABASE.save()

        with PRINT_LOCK:
            print('Saved database:\n', DATABASE)
        # TODO: info log
    
    # call a thread to save database every BACKUP_INTERVAL seconds
    t = Timer(BACKUP_INTERVAL, _save_database)
    t.daemon = True  # exit when server dies
    t.start()  # after BACKUP_INTERVAL seconds

if __name__ == '__main__':
    # --- server boot up ---

    # initialize the database
    DATABASE = Database()
    # start back-up procedure
    _save_database()
    

    # open a socket, listen for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind( (HOST, PORT_NUMBER) )
    server_socket.listen(5)

    with PRINT_LOCK:
        print('Server: created and bound the socket. Listening...\n')

    # --- main loop of the server ---
    while True:
        # accept a connection
        client_socket, addr = server_socket.accept()

        with PRINT_LOCK:
            print('\nAccepted the client')
            print('Address:', addr)
        # TODO: info log
        
        # allocate a client thread to deal with the client
        _thread.start_new_thread(
            _handle_client, 
            (client_socket,)
            )
