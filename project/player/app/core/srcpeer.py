########################################################################################################################
# @ Module : Source Peer
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all Candidate Peers/Players  protocols
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import socket
import json
from project.player.app.utilites.netutils import Netutils


class SrcPeer:
    ####################################################################################################################
    #                                        SOURCE/CANDIDATE PEER MODULE
    ####################################################################################################################

    def __init__(self, peer_ip, peer_port):
        """
        *****************************************
        Overloaded Constructor

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.peer_socket = None

    def ping(self):
        """
        *****************************************
        Method used to ping candidate Peer

        :return:
        *****************************************
        """
        command = "PING"

        # Sending <Ping> Request to Candidate Peer ...
        self.sock_write(command)

        # Reading Response from Candidate Peer ...
        response = self.sock_read()

        # Decoding response from Candidate Peer ...
        if response == "200":
            return True
        else:
            return False

    def get_available_books(self, library_id):
        """
        *****************************************
        Method used to discover all books
            a candidate peer might have

        :param: library_id: String
        :return: List <Libraries>
        *****************************************
        """
        command = "GET_AVAILABLE_BOOKS {}".format(library_id)

        # Sending <GetAvailableBooks> Request to Candidate Peer ...
        self.sock_write(command)

        # Reading Response from Candidate Peer ...
        response = self.sock_read()

        # Decoding response from Candidate Peer ...
        response_parts = response.split()

        if response_parts[0] == "200":
            list_of_available_books = json.loads(response_parts[1])
            return [True, list_of_available_books]
        elif response_parts[0] == "500":
            return [False, "Candidate Server Error "]
        else:
            return [False, "Unknown Exception occured while getting books from Candidate peer"]

    def request_book(self, library_id, book_id):
        """
        *****************************************
        Method used to request a book from a
            candidate peer
        
        :param library_id:
        :param book_id: 
        :return:
        *****************************************
        """
        command = "REQUEST_BOOK {} {}".format(library_id, book_id)

        # Sending <RequestBook>  to Candidate Peer ...
        self.sock_write(command)

        # Reading Response from Candidate Peer ...
        response = self.sock_read()

        # Decoding response from Candidate Peer ...
        response_parts = response.split()

        if response_parts[0] == "200":
            bytes_res = response_parts[1]
            return [True, bytes_res]
        elif response_parts[0] == "500":
            return [False, "Candidate Server Error "]
        elif response_parts[0] == "600":
            return [False, "Book Not Available"]
        elif response_parts[0] == "600":
            return [False, "Candidate Peer is Busy"]
        else:
            return [False, "Unknown Exception occured while getting books from Candidate peer"]

    def connect(self):
        """
        *****************************************
        Method used to connect to peer

        :return: Boolean
        *****************************************
        """
        try:
            self.peer_socket = socket.create_connection((self.get_peer_ip(), self.get_peer_port()))
            return True
        except Exception:
            return False

    def disconnect(self):
        """
        *****************************************
        Method used to disconnect from peer

        :return: Boolean
        *****************************************
        """
        self.peer_socket.close()

    def get_peer_port(self):
        """
        *****************************************
        Method used to  get a candidate peer port

        :return: Integer
        *****************************************
        """
        return self.peer_port

    def get_peer_ip(self):
        """
        *****************************************
        Method used to  get a candidate peer ip
            address

        :return: Integer
        *****************************************
        """
        return self.peer_ip

    def sock_write(self, str_to_send):
        """
        *****************************************
        Method used to send a request/command to
            Candidate Peer

        :param: str_to_send
        :return: Boolean
        *****************************************
        """

        self.peer_socket.sendall(str.encode("{}\r\n".format(str_to_send)))
        return True

    def sock_read(self, timeout = None):
        """
        *****************************************
        Method used to  read response from
        Candidate peer

        :return: String [UTF-8]
        *****************************************
        """
        return Netutils.read_line(self.peer_socket)

    ####################################################################################################################
    #                                    END OF SOURCE/CANDIDATE PEER MODULE
    ####################################################################################################################
