########################################################################################################################
# @ Module : Peer
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all Incoming Peers/Players  protocols
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import socket
import json
from threading import Thread

from project.player.app.utilites.netutils import Netutils


class InPeer:
    ####################################################################################################################
    #                                         INCOMING   PEER MODULE
    ####################################################################################################################

    incoming_peer_length = 0

    def __init__(self, peer_socket, peer_address):
        """
        *****************************************
        Overloaded Constructor

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        self.peer_address = peer_address
        self.peer_socket = peer_socket
        self.peer_last_request_datetime = None
        InPeer.incoming_peer_length = InPeer.incoming_peer_length + 1

    def handle_request(self):
        """
        *****************************************
        Method used to handle all requests from
        the incoming peer

        :return: Boolean
        *****************************************
        """
        def handle(peer_socket):

            while True:
                try:
                    line = Netutils.read_line(self.peer_socket)
                    print("\nCommand IN: {} ".format(line))
                    if line is None:
                        print("Client disconnecting ...")
                        InPeer.incoming_peer_length = InPeer.incoming_peer_length - 1
                        break

                    # Handling command
                    line_parts = line.split()
                    command = line_parts[0]

                    # PING
                    if command == "PING":
                        response_to_send = "200"
                        peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                        print("\nCommand OUT: {} ".format(response_to_send))

                    # GET AVAILABLE BOOK
                    elif command == "GET_AVAILABLE_BOOKS":
                        response_to_send = "200 []"
                        peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                        print("\nCommand OUT: {} ".format(response_to_send))

                    # REQUEST BOOK
                    elif command == "REQUEST_BOOK":
                        response_to_send = "200 []"
                        peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                        print("\nCommand OUT: {} ".format(response_to_send))

                    else:
                        response_to_send = "500"
                        peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                        print("\nCommand OUT: {} ".format(response_to_send))
                except:
                    response_to_send = "500"
                    peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                    print("\nCommand OUT: {} ".format(response_to_send))
                    print("Exception occured.  disconnecting ...")
                    break

        t = Thread(target=handle, args=[self.peer_socket])
        return t



    # Handle Ping
    def disconnect(self):
        """
        *****************************************
        Method used to disconnect from peer

        :return: Boolean
        *****************************************
        """
        self.peer_socket.close()

    def get_peer_address(self):
        """
        *****************************************
        Method used to  get a candidate peer
            address

        :return: Integer
        *****************************************
        """
        return self.peer_address

    ####################################################################################################################
    #                                    END OF  INCOMING PEER MODULE
    ####################################################################################################################
