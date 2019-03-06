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
import json
import os
from pathlib import Path
from threading import Thread
from app.librarifier.stuff import Stuff
from app.settings.config import Config
from app.utilites.auxiliaries import Auxiliaries
from app.utilites.netutils import Netutils
from random import shuffle

class InPeer:
    ####################################################################################################################
    #                                         INCOMING   PEER MODULE
    ####################################################################################################################

    incoming_peer_length = 0
    loaded_stuffs = dict()

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
                    Auxiliaries.console_log("\nCommand IN: {} ".format(line))
                    if line is None:
                        Auxiliaries.console_log("Client disconnecting ...")
                        InPeer.incoming_peer_length = InPeer.incoming_peer_length - 1
                        break

                    # Handling command
                    line_parts = line.split()
                    command = line_parts[0]

                    req_args = []
                    if len(line_parts) > 1:
                        req_args = line_parts[1:]

                    # PING
                    if command == "PING":
                        response_to_send = self.ping_response(req_args)
                        peer_socket.sendall(response_to_send)
                        Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                    # GET AVAILABLE BOOK
                    elif command == "GET_AVAILABLE_BOOKS":
                        response_to_send = self.get_available_books_response(req_args)
                        peer_socket.sendall(response_to_send)
                        Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                    # REQUEST BOOK
                    elif command == "REQUEST_BOOK":
                        response_to_send = self.get_book_response(req_args)
                        peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                        # Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                    else:
                        response_to_send = "400"
                        peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                        Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))

                except Exception as e:
                    response_to_send = "500"
                    peer_socket.sendall(str.encode("{}\r\n".format(response_to_send)))
                    Auxiliaries.console_log("\nCommand OUT: {} ".format(response_to_send))
                    Auxiliaries.console_log("Exception occurred.  disconnecting ...")
                    break

        t = Thread(target=handle, args=[self.peer_socket])
        return t

    def ping_response(self, args = None):
        """
        *****************************************
        Method used to handle ping request

        :return: String Encoded
        *****************************************
        """
        response_to_send = "200"
        return str.encode("{}\r\n".format(response_to_send))

    def get_available_books_response(self, args ):
        """
        *****************************************
        Method used to handle get available books
            response

        :return: String Encoded
        *****************************************
        """
        try:
            # get args
            if len(args) != 1:
                response_to_send = "401"
                return self.reply(response_to_send)

            library_id = args[0]
            stuff = self.load_stuff(library_id)

            # In case library_id does not exist
            if stuff is None:
                response_to_send = "402"
                return self.reply(response_to_send)

            availableBooks = list(stuff.get_list_book_received())
            shuffle(availableBooks)
            res_data = json.dumps(availableBooks)
            Auxiliaries.console_log(res_data)
            res_data_length = len(res_data)

            response_to_send = "200 {} {}".format(res_data_length, res_data)
            Auxiliaries.console_log(response_to_send)
            return self.reply(response_to_send)

        except Exception as e:
            Auxiliaries.console_log("Exception Occurred {}".format(e))
            response_to_send = "500"
            return self.reply(response_to_send)


    def get_book_response(self,args = None ):
        """
        *****************************************
        Method used to handle get  books
            response

        :return: String Encoded
        *****************************************
        """
        try:
            # get args
            if len(args) != 2:
                response_to_send = "401"
                return self.reply(response_to_send)

            library_id = args[0]

            stuff = self.load_stuff(library_id)

            # In case library_id does not exist
            if stuff is None:
                response_to_send = "402"
                return self.reply(response_to_send)
            # in case book_id is not integer
            try:
                book_id = int(args[1])
            except Exception as ex:
                Auxiliaries.console_log("Exception Occurred", ex)
                response_to_send = "402"
                return self.reply(response_to_send)

            # Auxiliaries.console_log("total_number_of_books: {} ".format( str(stuff.total_no_books) ))
            if book_id >= stuff.total_no_books:
                Auxiliaries.console_log("Out of list index", book_id)
                response_to_send = "402"
                return self.reply(response_to_send)
            # Auxiliaries.console_log("before encoding: {} ".format(stuff.fetchBook(book_id).book_bytes))

            # ---
            res_data = list( stuff.fetchBook(book_id).book_bytes)
            # ---
            res_data_length = len(res_data)

            response_to_send = "200 {} {}".format( res_data_length, res_data)
            Auxiliaries.console_log("Replying with book id {} ".format( str(book_id)  ))
            return response_to_send

        except Exception as e:
            Auxiliaries.console_log("Exception Occurred: {} ".format(e) )
            response_to_send = "500"
            return self.reply(response_to_send)

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

    def reply(self,message):
        return str.encode("{}\r\n".format(message), "utf-8")

    def reply_no_eol(self,message):
        return str.encode("{}".format(message), "utf-8")

    def load_stuff(self, library_id):
        """
        *****************************************
        Method used to load stuff given a
        Library id

        :return: Integer
        *****************************************
        """
        if library_id not in InPeer.loaded_stuffs:
            stuff_file_path = Config.STUFFS_DIR + os.sep + library_id + ".pkl"
            stuff_file = Path(stuff_file_path)
            if stuff_file.exists():
                stuff_object = Stuff.load(stuff_file_path)
                InPeer.loaded_stuffs[library_id] = stuff_object
            else:
                return None

        return InPeer.loaded_stuffs[library_id]
    ####################################################################################################################
    #                                    END OF  INCOMING PEER MODULE
    ####################################################################################################################
