########################################################################################################################
# @ Module : Console
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : February 2019
# @ Desc   : This Module  implements all flows as seen by the user to manage/interact with  the application via cli
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import os

from app.services.distributor import Distributor
from app.core.tracker import Tracker
from app.librarifier.librarifier import Librarifier
from app.librarifier.stuff import Stuff
from app.settings.config import Config


class Console:
    ####################################################################################################################
    #                                         CONSOLE   MODULE
    ####################################################################################################################



    def __init__(self):
        """
        *****************************************
        Overloaded Constructor

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        pass

    def launch(self):
        """
        *****************************************
        Method use to launch the Consle Application

        :param peer_ip: String
        :param peer_port: Integer
           *****************************************
        """
        pass



    #########
    # MENU
    #########

    def main_menu(self):
        """
        *****************************************
        Method use to launch the Consle Application

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        pass


    def help_menu(self ):
        """
        *****************************************
        Help commend

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        pass

    ##############
    # AUXILIARIES
    #############

    def upload_library(self):
        """
        *****************************************
        Upload Library command

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        hub_address = Config.HUB_IP+":"+str(Config.HUB_PORT)

        output_folder_path = Config.LIBS_DIR
        print(output_folder_path )

        # Input | Input File Path # eg: /media/betek/LENOVO/solve_ai.mp3
        input_file_path = input("Enter Input File path: ")
        try:
           status, library_id,  output_file_path = Librarifier.librarify(input_file_path, hub_address,1024,output_folder_path)

           if status is True :
               # Build Stuff for that Library ...
               stuff  = Stuff(input_file_path)
               stuff_file_path = Config.STUFFS_DIR + os.sep + library_id + ".pkl"
               stuff.persist(stuff_file_path)
               # TODO: Push output file  on Remote Repository

               # TODO: Register myself as a peer for that library
               tracker = Tracker(Config.HUB_IP, Config.HUB_PORT)
               tracker.register_peer(library_id, Distributor.get_ip(), Distributor.get_port())

               print("OK | Library was successfully uploaded. outpuFilePath",output_file_path)
           else:
               print("Failed | Unable to upload File" )
        except Exception as e:
            print("Exception occured while uploading Library")

        return


    #Library
        # View all Libraries
        # Upload Library
        # Download a library

    # Download
        # On Hold
        # In progress
        # Completed

    # Logs
        # Event
        # Error

    # Services
        # - Requestor
        # - Distributor

    # Settings
        # show all all vars  and select the one to modify

    # About
    # Exit


    ####################################################################################################################
    #                                    END OF CONSOLE   MODULE
    ####################################################################################################################

if __name__ == "__main__":
    cli = Console()
    cli.upload_library()