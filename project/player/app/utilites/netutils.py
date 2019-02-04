########################################################################################################################
# @ Module : Netutils
#
# @ Author : EMMA (Group J)
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
import  socket


class Netutils:
    ####################################################################################################################
    #                                           PEER MODULE
    ####################################################################################################################

    def __init__(self):
        """
        *****************************************
        Default Class

        *****************************************
        """
        pass


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
                res += b"\r";
            if b == b"\r":
                was_r = True;
            else:
                was_r = False;
                res += b;
        return res.decode("utf-8")
