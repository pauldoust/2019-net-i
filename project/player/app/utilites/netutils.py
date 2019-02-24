########################################################################################################################
# @ Module : Netutils
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all networks related helper functions
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import socket
import time


class Netutils:
    ####################################################################################################################
    #                                           NETUTILS MODULE
    ####################################################################################################################

    @staticmethod
    def read_line(f):
        """
        *****************************************
        Method used to read line from a socket
        @ref: UJM | Computer Network Lab


        :param:f: socket
        :return String [UTF-8 ]

        *****************************************
        """
        res = b""
        was_r = False
        while True:
            b = f.recv(1)
            if len(b) == 0:
                return None
            if b == b"\n" and was_r:
                break
            if was_r:
                res += b"\r"
            if b == b"\r":
                was_r = True
            else:
                was_r = False
                res += b
        return res.decode("utf-8")


    @staticmethod
    def get_my_local_ip():
        """
        *****************************************
           Method used to get IP Address on Local
           Network

           :return String [UTF-8 ]

        *****************************************
        """
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return str(IPAddr)

    @staticmethod
    def get_my_remote_ip():
        """
        *****************************************
           Method used to get Remote IP Address
           Network

           :return String [UTF-8 ]

        *****************************************
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


    @staticmethod
    def get_timestamp():
        """
        *****************************************
           Method used to generate a timestamp
           eg: 1589164318

           :return String [UTF-8 ]

        *****************************************
        """
        return str(int(time.time()))


    @staticmethod
    def diff_list(list_a, list_b) :
        if len(list_a) > len(list_b):
            return  list( set(list_a) - set(list_b))
        else:
            return list(set(list_b) - set(list_a))


    ####################################################################################################################
    #                                          END NETUTILS MODULE
    ####################################################################################################################
