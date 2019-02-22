"""
To bring hub on-line, just run this. To connect, peers must know your IP
and PORT.

DESCRIPTION
    Hub module keeps track of available peers and handles their requests.

    Hub maintains a database to keep track of libraries and corresponding 
    lists of peers. While running, it accepts a connection and allocates 
    a thread to deal with further communication. 

    Once accepted, hub tries to receive a message from a client, decode it
    into a request and then execute the request.

1 + 1 + 1 + 1 + 1 + 1 + 1

Note:
    - think about one point of control and error resolution
    - database persistence
    - abstract the database?
    - fixed length for library id
"""

import _thread
import copy
import json
import random
import socket
import time


# --- constants used ---
CODEC = 'utf8'
# TODO: figure out what the heck is the host
HOST = ' '  # all available interfaces
PORT_NUMBER = 7777
# timeout time, in seconds - saw like 10 mins somewhere
TIMEOUT = 60.
PEER_COUNT = 10
# end-of-message antics
BEFORE_END_FLAG = b'\r'
END_SYMBOL = b'\n'
MESSAGE_END = BEFORE_END_FLAG + END_SYMBOL
# maximum message length is 1 Mb
MAX_MESSAGE_LENGTH = 1024**2


# -- ad hoc print for diagnostics ---
PRINT_LOCK = _thread.allocate_lock()

# --- server status codes ---
b_OK = b'200'
b_BUSY = b'300'
b_INVALID_COMMAND = b'400'
b_INVALID_SYNTAX = b'401'
b_INVALID_ARGUMENTS = b'402'
b_SERVER_ERROR = b'500'

# allocate the lock for our data structure
DATABASE_LOCK = _thread.allocate_lock()


# --- client thread function ---
def _handle_client(client_socket):
    """Receives and handles client's request, then closes the socket.
    
    Function reads data from client_socket, decodes and reads the request. 
    Based on the request, calls necessary procedure to execute it. 
    Then, closes the connection.

    If exception is raised in any of the methods called from here, it
    catches exception, sends back the error code, closes the socket 
    and re-raises exception to exit the thread.

    Params:
    ------
    client_socket -- alive socket connection with the client
        Client is expected to send the request, otherwise he times out.
    """
    
    # read data from TCP socket (binary stream)
    try:
        data = _read_data(client_socket)
    # close, send code and raise error if timed out or message is too big
    except (MemoryError, TimeoutError):
        client_socket.sendall(b_SERVER_ERROR + MESSAGE_END)
        client_socket.close()
        raise

    # decode the message into (hopefully) a request string
    data = data.decode(CODEC)

    # based on the data string, try to resolve the request
    try:
        _resolve(request=data, client_socket=client_socket)
    except ValueError:
        client_socket.sendall(b_INVALID_COMMAND + MESSAGE_END)
        client_socket.close()
        raise
    
    # gracefully close the connection
    client_socket.close()


# --- helper functions ---
def _read_data(client_socket):
    """Reads from sock until delimiter and returns a binary string received.

    Reads byte by byte from client_socket until MESSAGE_END is seen.

    Raises MemoryError if message is too long.

    Raises TimeoutError if client socket times out after TIMEOUT seconds.
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

# _resolve function (request, client_socket)
def _resolve(request, client_socket):
    """Based on the request, calls other functions to satisfy it.
    
    Given a REGISTER_PEER request, registers a peer.

    Given a LIST_PEERS request, sends back a list of peers.

    Raises ValueError if request does not follow the format.
    
    Params:
    ------
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

    # if the word does not correspond to known COMMAND, raise error
    else:
        raise ValueError('Invalid request.')

def _register_peer(request, client_socket):
    """Adds a peer to the database.
    
    Given a REGISTER_PEER request, acquires DATABASE_LOCK and adds a peer to
    the DATABASE. On success, sends code back using client_socket.

    Raises ValueError if request format is invalid.
    
    Params:
    ------
    request -- string of form 'REGISTER_PEER {library} {IPv4} {port}'
    client_socket -- alive socket connection with the client   
    """

    # TODO: make sure request is correct
    # parse the request
    try:
        _, library_ID, peer_ip, peer_port = request.split(' ')
    
    except:
        raise ValueError('Invalid request syntax.')


    # TODO: check the correctness of peer ipv4+port combo
    # TODO: check correctness of library_ID

    # get peer ip+port, create a peer dictionary object
    peer_ID = {'peer_ip': str(peer_ip),
               'peer_port': str(peer_port)}
        
    # TODO: better databases interaction - initialize empty array in dict
    # TODO: adding duplicate peer_IDs
    
    # with lock, add the peer to correct library (create new one if necessary)
    with DATABASE_LOCK:

        # if no library-list combo in DATABASE, add new list
        if DATABASE.get(library_ID, None) is None:
            DATABASE[library_ID] = []

            with PRINT_LOCK:
                print('\nCreated new library for file', library_ID)

        # append peer_ID to the list
        DATABASE[library_ID].append(peer_ID)
        with PRINT_LOCK:
                print('\nAdded peer ', peer_ID, 'to ', library_ID)

    # return the 'OK' response to the peer using client_socket
    client_socket.sendall(b_OK + MESSAGE_END)

def _list_peers(request, client_socket):
    """Sends json-encoded list of peers through the client_socket.
    
    Given a LIST_PEERS request, acquires DATABASE_LOCK, samples
    PEER_COUNT peers from DATABASE, serializes the list into the json
    string and sends it back using client_socket.

    Raises ValueError if request format is invalid.
    
    Params:
    ------
    request -- string of form 'LIST_PEERS {library}'
    client_socket -- open socket connection with the client   
    """

    # get the library id/name
    splitted_request = request.split()
    try:
        library_ID = splitted_request[1]
    except:
        raise ValueError('Request format is invalid')
        
    # with the lock,
    # get the subset of peer ip+port items from our database
    sample_peers = []

    with DATABASE_LOCK:
        result_list = DATABASE.get(library_ID, None)

        # if there is something in the database
        if result_list is not None:

            # more than PEER_COUNT peers available
            if len(result_list) > PEER_COUNT:
                sample_peers = random.sample(result_list, PEER_COUNT)
            # less than PEER_COUNT peers available
            else:
                sample_peers = copy.deepcopy(result_list[:])

        # on empty library, send back empty lsit
        else:
            sample_peers = []

    with PRINT_LOCK:
        print('\nSampled peers are', sample_peers)

    # put it in json string
    json_result = json.dumps(
        sample_peers,
        sort_keys=True,
        separators=(',', ': ')
        )
    
    # construct the response
    response = b_OK + b' ' + json_result.encode(CODEC) + MESSAGE_END
    
    # send the response to the client
    client_socket.sendall(response)

    with PRINT_LOCK:
        print('Sent the response', response)    


if __name__ == '__main__':
    # --- server boot up ---

    # TODO: isolate database in a class?
    # allocate data structure to keep track of libraries
    # and their corresponding peer lists
    DATABASE = {}

    # open a socket, listen for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind( (HOST, PORT_NUMBER) )
    print('Server: created and bound the socket. Listening...\n')
    server_socket.listen(5)

    # TODO: deal with server shutdown killing threads
    # --- main loop of the server ---
    while True:
        # accept a connection
        client_socket, addr = server_socket.accept()

        with PRINT_LOCK:
            print('\nAccepted the client')
            print('Address:', addr)

        # allocate a client thread to deal with the client
        _thread.start_new_thread(
            _handle_client, 
            (client_socket,)
            )

        # *back-up procedure, maybe
