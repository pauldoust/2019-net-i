########################################################################################################################
# @ Module : DummyCandidatePeer
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  emulates a Candidate Peer (Peer that provided needed library book(s) )
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################

from threading import Thread

from app.core.inpeer import InPeer
from app.utilites.netutils import Netutils
import socket
import json

def main():
    handle_acceptall().start()


def handle_acceptall():
    def handle():
        # create a socket that listens (on a port of your choice)
        server_socket = socket.socket()
        # accept new clients connections,
        # and start a handle_client thread every time
        server_socket.bind(("127.0.0.1", 5001))
        Auxiliaries.console_log("Starting Dummy Server ...")
        server_socket.listen()
        Auxiliaries.console_log("Dummy Server Started")
        while True:

            client_con, client_address = server_socket.accept()
            Auxiliaries.console_log("Client connected ...")
            Auxiliaries.console_log("Incoming peer length", InPeer.incoming_peer_length)
            incoming_peer = InPeer(client_con, client_address)
            #incoming_peer.handle_request().start()
            handle_client(client_con).start()

    t = Thread(target=handle)
    return t


# handle_client returns a Thread that can be started, i.e., use: handle_client(.......).start()
def handle_client(socket):
    def handle():

        while True:
            try:
                line = Netutils.read_line(socket)
                Auxiliaries.console_log("\nCommand IN: {} ".format(line))
                if line is None:
                    Auxiliaries.console_log("Client disconnecting ...")
                    break

                # Handling command
                line_parts = line.split()
                command = line_parts[0]

                # PING
                if command == "PING":
                    response_to_send = "200"
                    socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                    Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                # GET AVAILABLE BOOK
                elif command == "GET_AVAILABLE_BOOKS":
                    response_to_send = "200 []"
                    socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                    Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                # REQUEST BOOK
                elif command == "REQUEST_BOOK":
                    response_to_send = "200 []"
                    socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                    Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                else:
                    response_to_send = "500"
                    socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                    Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))
            except:
                response_to_send = "500"
                socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))
                Auxiliaries.console_log("Exception occured.  disconnecting ...")
                break

    t = Thread(target=handle)
    return t

if __name__ == "__main__":
    main()
