"""
DESCRIPTION
    Hub module keeps track of available peers and handles their requests.

    While running, it accepts a connection and allocates thread to deal
    with further communication. It maintains the database to keep track of
    files and corresponding lists of peers.

    TODO
1 + 1 + 1"""

import _thread
import json
import random
import socket
import time


# --- constants used ---
CODEC = 'utf8'
HOST = ''  # all available interfaces
PORT_NUMBER = 7777
# timeout time, in seconds - saw like 10 mins somewhere
TIMEOUT = 60.
BEFORE_END_FLAG = b'\r'
END_SYMBOL = b'\n'
MESSAGE_END = BEFORE_END_FLAG + END_SYMBOL
PEER_COUNT = 10

# --- server codes ---
# TODO

# allocate the lock for our data structure
DATABASE_LOCK = _thread.allocate_lock()

PRINT_LOCK = _thread.allocate_lock()

# --- client thread function (client_socket) ---
def _handle_client(client_socket):
    """From given socket, reads, deciphers the request, delegates work and closes.
    
    Function reads data from client_socket byte by byte until MESSAGE_END is seen, 
    assembles message, decodes and reads the request. Based on the request, 
    calls necessary procedure to satisfy the request. 
    Then, closes the connection.

    Params:
    ------
    client_socket -- open socket connection with the client
        Client is expected to send the request, so function waits for it
        TIMEOUT seconds, then raises timeout exception.
    """

    # wait for client data or time out
    client_socket.settimeout(TIMEOUT)

    try:

        # read stream byte by byte until next encountered sign is MESSAGE_END
        # TODO: how the fuck do I correctly get the whole message?
        is_flag_recieved = False

        # to aggregate the byte stream
        data = []

        while True:
            byte_recieved = client_socket.recv(1)

            # on '\r', expect the next byte to be '\n' to finish the msg
            if byte_recieved == BEFORE_END_FLAG:
                # TODO: problem with \rblabla\n strings
                
                is_flag_recieved = True
            # TODO: isolate into a routine to check if message has ended?

            elif (byte_recieved == END_SYMBOL) and is_flag_recieved == True:
                break
            
            else:
                data.append(byte_recieved)

    except TimeoutError:
        client_socket.sendall(b'500' + MESSAGE_END)
        client_socket.close()
        raise TimeoutError('Client connection timeout.')

    
    # arrange the data in one binary string to reconstruct original message
    data = b''.join(data)
    # decode the message into (hopefully) a request string
    data = data.decode(CODEC)
    
    # based on the data string, try to _ the request
    _resolve(request=data, client_socket=client_socket)

    # shutdown/close the connection
    client_socket.close()


# --- helper functions ---

# _resolve function (request, client_socket)
def _resolve(request, client_socket):
    """Based on request, calls other functions to satisfy it.
    
    Given a REGISTER_PEER request, registers a peer.
    Given a LIST_PEERS request, sends back a list of peers.
    
    Params:
    ------
    request -- raw string with (hopefully) correct request
    client_socket -- open socket connection with the client
        Is used to send back the codes and data.
    """

    # TODO: make sure request is valid

    # based on request (get the first word somehow), call proper function
    splitted_request = request.split()
    request_to_check = str(splitted_request[0]).lower()

    if request_to_check == 'register_peer':

        if len(splitted_request) == 4:
            _register_peer(request, client_socket)
        
        else:
            # error code
            client_socket.sendall(b'500' + MESSAGE_END)

    # elif the request is to list the peers
    if request_to_check == 'list_peers':

        if (len(splitted_request) == 2):
            _list_peers(request, client_socket)

        else:
            client_socket.sendall(b'500' + MESSAGE_END)

    else:
        # unknown request - send back error message
        client_socket.sendall(b'500' + MESSAGE_END)

def _register_peer(request, client_socket):
    """Adds a peer to the database.
    
    Given a REGISTER_PEER request, acquires DATABASE_LOCK and adds a peer to
    the DATABASE. Returns the code back using client_socket.
    
    Params:
    ------
    request -- string of form 'REGISTER_PEER {library} {IPv4} {port}'
    client_socket -- open socket connection with the client   
    """

    # TODO: make sure request is correct
    # parse the request
    _, library_ID, peer_ip, peer_port = request.split(' ')

    # TODO: check the correctness of peer ipv4+port combo
    # TODO: check correctness of library_ID

    # get peer ip+port, concatenate in 1 string
    peer_ID = str(peer_ip) + ':' + str(peer_port)
        
    # TODO: better databases interaction - initialize empty array in dict
    # with lock, add the peer to correct library
    with DATABASE_LOCK:
        # if no library-list combo in DATABASE, add new list
        if DATABASE.get(library_ID, None) is None:
            DATABASE[library_ID] = []

        # append peer_ID to the list
        DATABASE[library_ID].append(peer_ID)

    # return the 'OK' response to the peer using client_socket
    client_socket.sendall(b'200' + MESSAGE_END)

def _list_peers(request, client_socket):
    """Sends json-encoded list of peers through the client_socket.
    
    Given a LIST_PEERS request, acquires DATABASE_LOCK, samples
    PEER_COUNT peers from DATABASE, serializes the list into the json
    string and sends it back.
    
    Params:
    ------
    request -- string of form 'LIST_PEERS {library}'
    client_socket -- open socket connection with the client   
    """

    # get the library id/name
    splitted_request = request.split()
    library_ID = splitted_request[1]
        
    # with the lock,
    # get the subset of peer ip+port items from our database
    sample_peers = []

    with DATABASE_LOCK:
        nonlocal sample_peers
        # TODO: default should be None, but it breaks next line of code
        result_list = DATABASE.get(library_ID, [])

        if len(result_list) > 0:

            # more than PEER_COUNT peers available
            if len(result_list) > 10:
                sample_peers = random.sample(result_list, PEER_COUNT)
            # less than PEER_COUNT peers available

            else:
                # TODO: deepcopy here? peer list might contain something mutable
                sample_peers = result_list[:]

        else:
            client_socket.sendall(b'500' + MESSAGE_END)
            return

        # make sure we de-reference shared DATABASE
        result_list = None

    # put it in json string
    json_result = json.dumps(
        sample_peers,
        sort_keys=True,
        separators=(',', ': ')
        )
    
    # construct the response
    response = b'200 ' + json_result.encode(CODEC) + MESSAGE_END
    
    # send the response to the client
    client_socket.sendall(response)


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
start = 0
while True:
    # accept a connection
    client_socket, _ = server_socket.accept()

    # allocate a client thread to deal with the client
    _thread.start_new_thread(
        _handle_client, 
        (client_socket,)
        )

    # *back-up procedure, maybe
    if start - time.time() >= 30:
        with PRINT_LOCK:
            print('\n\n\nCurrent DATABASE\n')
            print(DATABASE)
        start = 0
