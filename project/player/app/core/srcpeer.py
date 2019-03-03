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
import base64
import socket
import json
from threading import Thread
import  time

from app.librarifier.book import Book
from app.utilites.auxiliaries import Auxiliaries
from app.utilites.netutils import Netutils


class SrcPeer:
    ####################################################################################################################
    #                                        SOURCE/CANDIDATE PEER MODULE
    ####################################################################################################################

    def __init__(self,  peer_ip, peer_port ):
        """
        *****************************************
        Overloaded Constructor

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """

        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.peer_id = str(peer_ip)+":"+str(self.peer_port)
        self.peer_socket = None
        self.activity_flag = True

    def ping(self):
        """
        *****************************************
        Method used to ping candidate Peer

        :return:
        *****************************************
        """
        command = "PING"
        Auxiliaries.console_log("writing to socket ...")
        # Sending <Ping> Request to Candidate Peer ...
        self.sock_write(command)
        Auxiliaries.console_log("waiting for socket response ...")
        # Reading Response from Candidate Peer ...
        response = self.sock_read()

        Auxiliaries.console_log(response)
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
        response_parts = response.split(" ")

        res_code = str(response_parts[0])
        res_data = None
        res_data_length = 0

        if res_code == "200":
            res_data_length = int(response_parts[1])
            res_data = str.join("",response_parts[2:])

        return res_code, res_data_length, res_data

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
        """
        response = response.split("b\'")[1]
        response_parts = response.split(" ")
        Auxiliaries.console_log(response_parts)

        res_code = response_parts[0]

        Auxiliaries.console_log(res_code)
        res_data = None
        res_data_length = 0

        if res_code == "200":
            res_data_length = int(response_parts[1])
            res_data =  str.join("",response_parts[2:]).split("\\r\\n")[0]
            res_data =  res_data.replace("\\\\x","\\x")
            res_data = res_data.replace("\\\'", "\'")
            res_data = res_data.replace("bytearray(b\'","")
            res_data = res_data.replace("\')", "")
            res_data = bytearray(res_data,"utf-8")

        """
        response_parts = response.split(" ")

        #Auxiliaries.console_log(response_parts)
        Auxiliaries.console_log("book received")

        res_code = response_parts[0].replace("b\"","")

        Auxiliaries.console_log(res_code)
        res_data = None
        res_data_length = 0

        if res_code == "200":
            res_data_length = int(response_parts[1])
            res_data= str.join("",response_parts[2:]).replace("\\r\\n", "")
            res_data= res_data.replace("b\'","").replace("\"","")
            res_data = base64.b64decode(res_data)
            #Auxiliaries.console_log(repr(res_data) )

        return res_code, res_data_length, res_data

    def connect(self):
        """
        *****************************************
        Method used to connect to peer

        :return: Boolean
        *****************************************
        """
        try:
            #print(self.get_peer_ip())
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

        :return: String
        *****************************************
        """
        return self.peer_ip


    def get_peer_id(self):
        """
        *****************************************
        Method used to  get a candidate peer id


        :return: String
        *****************************************
        """
        return self.peer_id

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

    def set_activity_status(self, status):
        """
        *****************************************
        Method used to  get a activity status

        :param: status : Boolean
        :return: Void
        *****************************************
        """
        self.activity_flag = status

    def get_activity_status(self):
        """
        *****************************************
        Method used to  get a activity status

        :return: Boolean
        *****************************************
        """
        return self.activity_flag

    def download_job(self, _library_id, _collected_books , _stuff_obj ,_library_obj):
        """
        *****************************************
        Method used to run download job

        :param _library_obj:
        :param _collected_books:
        :param _stuff_obj:
        :return: Void
        *****************************************
        """

        def handle(_self, library_id, collected_books, stuff_obj, library_obj):
            Auxiliaries.console_log("starting  srcpeer download_job ... ")
            try:
                # Connect to peer ...
                if _self.connect() is False:
                    _self.set_activity_status(False)
                else:
                    # Ping/handshake ...
                    if _self.ping() is False:
                        _self.set_activity_status(False)

                while _self.get_activity_status():

                    # Requesting  available books ...
                    res_code, res_data_length, res_data = _self.get_available_books(_library_id)

                    available_books = list()

                    if res_code == "200":
                        available_books = json.loads(res_data)
                        #Auxiliaries.console_log("available_books", available_books)
                    else:
                        _self.set_activity_status(False)
                        break

                    # Checking missing books per what is already available in stuff ...
                    missing_book = Auxiliaries.diff_list( stuff_obj.get_list_book_received(), available_books)
                    Auxiliaries.console_log("list book already received", stuff_obj.get_list_book_received())
                    Auxiliaries.console_log("missing book", missing_book)
                    if len(missing_book) == 0:
                        Auxiliaries.console_log("No interresting available book(s) from you, I am not interested. bye")
                        _self.set_activity_status(False)
                        break

                    # Requesting for all the missing books till none are left ...
                    for book_id in missing_book:
                        Auxiliaries.console_log("requesting book id ...", book_id)
                        res_code, res_data_length, res_data = _self.request_book(library_id, book_id)

                        if res_code == "200":
                            book = res_data
                            Auxiliaries.console_log("received book :", book)
                            collected_books.append([book_id,book])


                    # Requesting books from peers


                    time.sleep(14)

                _self.set_activity_status(False)
                Auxiliaries.console_log("exiting  srcpeer  download_job... ", _self.get_peer_id())
            except Exception as e:
                Auxiliaries.console_log("Exception ", e)
                _self.set_activity_status(False)
                pass

        t = Thread(target=handle, args=[self, _library_id, _collected_books, _stuff_obj, _library_obj])
        return t

    ####################################################################################################################
    #                                    END OF SOURCE/CANDIDATE PEER MODULE
    ####################################################################################################################
