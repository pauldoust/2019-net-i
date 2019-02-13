########################################################################################################################
# @ Module : Distributor Service
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module implement the Peer/player socket server and manage all incoming Peers request
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################

from threading import Thread
from project.player.app.core.inpeer import InPeer
import socket
import random


class Distributor:
    ####################################################################################################################
    #                                          DISTRIBUTOR MODULE
    ####################################################################################################################
    def __init__(self, ):
        """
        *****************************************
        Default Constructor

        *****************************************
        """
        pass

    @staticmethod
    def start_service(distributor_port=None):
        if distributor_port is None:
            distributor_port = random.randrange(1023, 65535)

        Distributor.handle_accept_all(distributor_port).start()

    @staticmethod
    def handle_accept_all(distributor_port):
        def handle(port):
            server_socket = socket.socket()
            server_socket.bind(("127.0.0.1", port))
            print("Starting Distributor Server ...")
            server_socket.listen()
            print("Distributor Server Started")
            while True:

                client_con, client_address = server_socket.accept()
                print("Client connected ...")
                print("Current peer connected count ", InPeer.incoming_peer_length)
                incoming_peer = InPeer(client_con, client_address)
                incoming_peer.handle_request().start()

        t = Thread(target=handle, args=[distributor_port])
        return t

    ####################################################################################################################
    #                                        END DISTRIBUTOR MODULE
    ####################################################################################################################
