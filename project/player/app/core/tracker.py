########################################################################################################################
# @ Module : Tracker
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all communication between the player and the tracker
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import socket
import json

from app.utilites.auxiliaries import Auxiliaries
from app.utilites.netutils import Netutils


class Tracker:
    ####################################################################################################################
    #                                              TRACKER  MODULE
    ####################################################################################################################

    def __init__(self, tracker_ip, tracker_port):
        """
        *****************************************
        Overloaded Constructor

        :param tracker_ip: String
        :param tracker_port: Integer
        *****************************************
        """
        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port
        self.tracker_socket = None

    def list_peers(self, library_id):
        """
        *****************************************
        Method used to list peers given a library id

        :return:
        *****************************************
        """
        command = "LIST_PEERS {}".format(library_id)
        Auxiliaries.console_log("writing to socket ...", command)
        # Sending <Ping> Request to Candidate Peer ...
        self.connect()
        self.sock_write(command)
        Auxiliaries.console_log("waiting for socket response ...")
        # Reading Response from Candidate Peer ...
        response_str = self.sock_read()
        #print(response_str)
        self.disconnect()
        Auxiliaries.console_log("reading response from socket ...", response_str)

        try:
            # Response format : 200 {length_resp} {resp}
            # Decoding response
            res_code = "500"
            res_data = None
            res_data_length = 0

            response_parts = response_str.split(" ")
            res_code = response_parts[0]
            if res_code == "200":
                res_data_length = int(response_parts[1])
                # Adapting to new protocol

                res_data = str.join("", response_parts[2:])

                res_data = json.loads(str(res_data) )
                #print("json_load", res_data)
                ip_port_lists = list()
                for objs in res_data :
                    ip_port_lists.append( str( objs['peer_ip'])+":"+ str(objs['peer_port']))

                res_data = json.dumps(ip_port_lists)

        except Exception as e:
            Auxiliaries.console_log("Error occurred while decoding response. Details: "+str(e))
            res_code = 500

        return res_code, res_data_length, res_data

    def register_peer(self, library_id, ip, port):
        """
        *****************************************
        Method used to register a peer to the tracker

        :param library_id:
        :param ip:
        :param port:
        :return:
        *****************************************
        """
        command = "REGISTER_PEER {} {} {}".format(library_id, ip, port)
        Auxiliaries.console_log("writing to socket ...", command)
        # Sending <Register peer> Request to Candidate Peer ...
        self.connect()
        self.sock_write(command)
        Auxiliaries.console_log("waiting for socket response ...")
        # Reading Response from Candidate Peer ...
        response = self.sock_read()
        self.disconnect()
        Auxiliaries.console_log("reading response from socket ...", response)
        Auxiliaries.console_log(response)
        # Decoding response from Candidate Peer ...
        if response == "200":
            return True
        else:
            return False


    def register_peer(self, library_id, ip, port):
        """
        *****************************************
        Method used to register a peer to the tracker

        :param library_id:
        :param ip:
        :param port:
        :return:
        *****************************************
        """
        command = "REGISTER_PEER {} {} {}".format(library_id, ip, port)
        Auxiliaries.console_log("writing to socket ...", command)
        # Sending <Register peer> Request to Candidate Peer ...
        self.connect()
        self.sock_write(command)
        Auxiliaries.console_log("waiting for socket response ...")
        # Reading Response from Candidate Peer ...
        response = self.sock_read()
        self.disconnect()
        Auxiliaries.console_log("reading response from socket ...", response)
        Auxiliaries.console_log(response)
        # Decoding response from Candidate Peer ...
        if response == "200":
            return True
        else:
            return False



    def delete_all_peer(self):
        """
        *****************************************
        Method used to register a peer to the tracker

        :param library_id:
        :param ip:
        :param port:
        :return:
        *****************************************
        """
        command = "DELETE "#.format(library_id, ip, port)
        Auxiliaries.console_log("writing to socket ...", command)
        # Sending <Register peer> Request to Candidate Peer ...
        self.connect()
        self.sock_write(command)
        Auxiliaries.console_log("waiting for socket response ...")
        # Reading Response from Candidate Peer ...
        response = self.sock_read()
        self.disconnect()
        Auxiliaries.console_log("reading response from socket ...", response)
        Auxiliaries.console_log(response)
        # Decoding response from Candidate Peer ...
        if response == "200":
            return True
        else:
            return False



    def connect(self):
        """
        *****************************************
        Method used to connect to peer

        :return: Boolean
        *****************************************
        """
        try:
            self.tracker_socket = socket.create_connection((self.get_tracker_ip(), self.get_tracker_port()))
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
        self.tracker_socket.close()

    def get_tracker_port(self):
        """
        *****************************************
        Method used to  get a candidate peer port

        :return: Integer
        *****************************************
        """
        return self.tracker_port

    def get_tracker_ip(self):
        """
        *****************************************
        Method used to  get a candidate peer ip
            address

        :return: Integer
        *****************************************
        """
        return self.tracker_ip

    def sock_write(self, str_to_send):
        """
        *****************************************
        Method used to send a request/command to
            Candidate Peer

        :param: str_to_send
        :return: Boolean
        *****************************************
        """

        self.tracker_socket.sendall(str.encode("{}\r\n".format(str_to_send)))
        return True

    def sock_read(self, timeout=None):
        """
        *****************************************
        Method used to  read response from
        Candidate peer

        :return: String [UTF-8]
        *****************************************
        """
        return Netutils.read_line(self.tracker_socket)

    ####################################################################################################################
    #                                       END OF TRACKER MODULE
    ####################################################################################################################
