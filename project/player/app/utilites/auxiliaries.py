########################################################################################################################
# @ Module : Auxiliaries
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  implements all general helper functions
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import glob
import os
import select
import sys
import platform
import sys
import time





class Auxiliaries:
    ####################################################################################################################
    #                                           AUXILIARIES MODULE
    ####################################################################################################################

    LOG_BUFFER =[]

    @staticmethod
    def diff_list(list_a, list_b):
        """
        *****************************************
           Method used to return the difference
           between two list

           :return String [UTF-8 ]

        *****************************************
        """
        if len(list_a) > len(list_b):
            return  list( set(list_a) - set(list_b))
        else:
            return list(set(list_b) - set(list_a))

    @staticmethod
    def parse_port( port_no):
        """
        *****************************************
           Method used to validate port no


           :return Boolean

        *****************************************
        """
        if port_no not in range(0, 65535):
            return False
        return True

    @staticmethod
    def parse_port( port_no):
        """
        *****************************************
           Method used to validate port no


           :return Boolean

        *****************************************
        """
        if port_no not in range(0, 65535):
            return False
        return True

    @staticmethod
    def console_log(*message):
        """
        *****************************************
        Method used to  display the log


           :return Boolean

        *****************************************
        """
        buffer_limit = 100
        # print(message)
        #print(message)

        #combined =  [list(row) for row in message]
        if len( Auxiliaries.LOG_BUFFER) > buffer_limit :
            Auxiliaries.LOG_BUFFER.pop(0)

        Auxiliaries.LOG_BUFFER.append(message)


    @staticmethod
    def scan_dir(dirPath):
        """
        *****************************************
        Upload Library command

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        # View all Library...
        os.chdir(dirPath)
        libs = []
        for file in glob.glob("*.lib"):
            libs.append(file)

        return libs

    @staticmethod
    def input_timeout( timeout ):
        """
        *****************************************
        Request an input from user with a countdown

        :param timeout: Integer
        :return: String | None in case timeout
        *****************************************
        """
        if Auxiliaries.get_os_name() == "WINDOWS":
            return Auxiliaries.input_timeout_win("",None,timeout)
        i, o, e = select.select([sys.stdin], [], [], timeout)

        if i:
            return sys.stdin.readline().strip()
        else:
            return None

    @staticmethod
    def input_timeout_win( caption, default, timeout = 5):
        """
        *****************************************
        Request an input from user with a countdown
            for Windows

        :param caption: 
        :param default: 
        :param timeout:
        :return: String | None in case timeout
        *****************************************
        """
        import msvcrt
        start_time = time.time()
        sys.stdout.flush()
        input = ''
        while True:
            if msvcrt.kbhit():
                byte_arr = msvcrt.getche()
                if ord(byte_arr) == 13: # enter_key
                    return ""
                elif ord(byte_arr) >= 32: #space_char
                    input += "".join(map(chr,byte_arr))
            if len(input) == 0 and (time.time() - start_time) > timeout:
                #print("timing out, using default value.")
                break

        #print('')  # needed to move to next line
        if len(input) > 0:
            return input
        else:
            return default



    @staticmethod
    def get_os_name():
        """
        *****************************************

        Method used to get the OS name

        :return: String
        *****************************************
        """
        return  str(platform.system()).upper()

    @staticmethod
    def isInteger(s):
        """
        *****************************************
        Method used check if string can be casted
        to int

        :return: String
        *****************************************
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    ####################################################################################################################
    #                                          END AUXILIARIES MODULE
    ####################################################################################################################

if __name__ == "__main__":
    #Auxiliaries.console_log("This is what I meant {} ".format("by"), 22)
    #from app.settings.config import Config
    #print(Auxiliaries.scan_dir( Config.LIBS_DIR ))
    print(Auxiliaries.get_os_name())