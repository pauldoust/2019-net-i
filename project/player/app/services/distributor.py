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
from app.core.inpeer import InPeer
import socket
import random
from app.settings.config import Config
from app.utilites.auxiliaries import Auxiliaries
from app.utilites.netutils import Netutils


class Distributor:
    ####################################################################################################################
    #                                          DISTRIBUTOR MODULE
    ####################################################################################################################

    port = 0
    status = False

    def __init__(self):
        """
        *****************************************
        Default Constructor

        *****************************************
        """
        pass

    @staticmethod
    def start_service(distributor_port=None):
        if distributor_port is None:
            distributor_port = Config.DISTRIBUTOR_PORT
        if str(distributor_port) == '0':
            distributor_port = random.randrange(1023, 65535)

        Config.DISTRIBUTOR_PORT = Distributor.port = distributor_port
        Distributor.handle_accept_all(Config.DISTRIBUTOR_PORT).start()
        return distributor_port

    @staticmethod
    def handle_accept_all(distributor_port):
        def handle(port):
            try:
                Distributor.port = port
                server_socket = socket.socket()
                Auxiliaries.console_log(port)
                server_socket.bind(("0.0.0.0", port))
                Auxiliaries.console_log("Starting Distributor Server ...")
                server_socket.listen()
                Auxiliaries.console_log("Distributor Server Started")
                Distributor.status = True
                while True:
                    client_con, client_address = server_socket.accept()
                    Auxiliaries.console_log("Client connected ...")
                    Auxiliaries.console_log("Current peer connected count ", InPeer.incoming_peer_length)
                    incoming_peer = InPeer(client_con, client_address)
                    incoming_peer.handle_request().start()
            except Exception as e:
                Auxiliaries.console_log("Exception", e)
            finally:
                Distributor.status = False

        t = Thread(target=handle, args=[distributor_port])
        return t

    @staticmethod
    def get_ip():
        # return "127.0.0.1"
        return Netutils.get_my_remote_ip()

    @staticmethod
    def get_port():
        return Distributor.port

    @staticmethod
    def get_service_status():
        return Distributor.status

    ####################################################################################################################
    #                                        END DISTRIBUTOR MODULE
    ####################################################################################################################

