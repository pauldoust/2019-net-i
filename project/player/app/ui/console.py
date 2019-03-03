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
import glob
import sys
from pathlib import Path
import time
from threading import Thread

from app.services.distributor import Distributor
from app.core.tracker import Tracker
from app.librarifier.librarifier import Librarifier
from app.librarifier.stuff import Stuff
from app.services.requestor import Requestor
from app.settings.config import Config
from app.utilites.auxiliaries import Auxiliaries


class Console:
    ####################################################################################################################
    #                                         CONSOLE   MODULE
    ####################################################################################################################
    LOADING_FLAG = False

    def __init__(self):
        """
        *****************************************
        Overloaded Constructor

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """
        pass

    #########
    # SETUP
    #########
    def setup(self):
        """
        *****************************************
        Method use to launch the Consle Application

        :param peer_ip: String
        :param peer_port: Integer
        *****************************************
        """

        # Creating data dir and related sub dirs if not yet done ...
        Console.app_title()
        print("\n\n")
        Console.start_loading("Loading modules ")
        try:
            Config.data_repo_inspection()

            # Is setup process already done ?
            if Config.is_setup() is True:
                time.sleep(2)
                Console.stop_loading()
                Console.start_loading("Initializing Setup Process ")
                time.sleep(3)
                Console.stop_loading()
                eval_bool = False
                warning_msg = "Invalid input. "
                error_detail= ""
                i = 0
                while eval_bool is False:
                    if i > 0:
                        print(warning_msg, error_detail)
                    response = input("Enter HUB IP (Enter skip to leave default value): ")
                    if response.lower() == "skip":
                        break
                    eval_bool, error_detail = Config.update_global_var("HUB_IP", response)

                error_detail = ""
                i = 0
                while eval_bool is False:
                    if i > 0:
                        print(warning_msg, error_detail)
                    response = input("Enter HUB PORT (Enter skip to leave default value): ")
                    if response.lower() == "skip":
                        break
                    eval_bool, error_detail = Config.update_global_var("HUB_PORT", response)

                error_detail = ""
                i = 0
                while eval_bool is False:
                    if i > 0:
                        print(warning_msg, error_detail)
                    response = input("Enter DISTRIBUTOR PORT (Enter skip to leave default value): ")
                    if response.lower() == "skip":
                        break
                    eval_bool, error_detail = Config.update_global_var("DISTRIBUTOR_PORT", response)

                Config.persist_setting()
                time.sleep(2)
                self.setup()

            return True
        finally:
            time.sleep(2)
            Console.stop_loading()
    def launch(self):
        """
        *****************************************
        Method use to launch the Consle Application

        :param peer_ip: String
        :param peer_port: Integer
           *****************************************
        """
        self.main_menu()
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
        # title
        # menu(options)
        # process

        while True:
            Console.app_title()
            Console.menu_title("Main Menu")
            print("Welcome to EMMA Torrent\n\n")

            print("1. Upload File")
            print("2. Download File")
            print("3. View Download ")
            print("4. View Logs ")
            print("5. View Services ")
            print("6. Settings ")
            print("7. About ")
            print("8. Exit ")

            choice = input("\n\nChoose an action: ")
            if str(choice) == "1":
                self.upload_library()
            elif str(choice) == "2":
                self.download_library()
            elif str(choice) == "3":
                self.view_downloads()
            elif str(choice) == "4":
                self.view_log()
            elif str(choice) == "5":
                self.view_services()
            elif str(choice) == "6":
                self.settings()
            elif str(choice) == "7":
                self.about()
            elif str(choice) == "8":
                self.exit_menu()
            elif str(choice).upper() == "EXIT":
                self.exit_menu()
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
        Console.app_title()
        Console.menu_title("Upload Library")

        print(" Enter <exit> to quit \n\n")

        hub_address = Config.HUB_IP+":"+str(Config.HUB_PORT)
        output_folder_path = Config.LIBS_DIR

        # Input | Input File Path # eg:/media/betek/LENOVO/solve_ai.mp3

        while True:
            choice = input("Enter Input File path: ")
            choice = choice.strip()
            if choice.upper() == "EXIT":
                return
            elif choice == "" :
                print("No filename provided")
            elif Path(choice).exists() is True :
                input_file_path = choice
                break
            else:
                print("File [{}] does not exit".format(choice))

        try:
            # print("(1/3) Creating Lib File ....")
            Console.start_loading("(1/3) Creating Lib File ")
            status, library_id, output_file_path = Librarifier.librarify(input_file_path, hub_address, 1024, output_folder_path)
            time.sleep(3)
            if status is True :
                Console.stop_loading()
                print("(1/3) Lib File successfully Created ")
                # print("(1/3) Lib File successfully Created ", end="\r")
                time.sleep(1)
                Console.start_loading("(2/3) Creating Stuff File ")

                # Build stuff for that library...
                stuff  = Stuff(input_file_path)
                stuff_file_path = Config.STUFFS_DIR + os.sep + library_id + ".pkl"
                stuff.persist(stuff_file_path)
                time.sleep(3)
                Console.stop_loading()
                print("(2/3) Stuff File successfully Created       ")
                # print("(2/3) Stuff File successfully Created ",end="\r")
                time.sleep(1)
                # TODO: Push output file  on Remote Repository

                # TODO: Register myself as a peer for that library
                Console.start_loading("(3/3) Registering  Peer on Hub")
                tracker = Tracker(Config.HUB_IP, Config.HUB_PORT)
                tracker.register_peer(library_id, Distributor.get_ip(), Distributor.get_port())
                time.sleep(2)
                Console.stop_loading()
                print("(3/3) Peer successfully registered on Hub")

                print("\n\n[OK]: Library was successfully uploaded. outpuFilePath [{}] ".format(output_file_path) )

            else:
                print("\n\n[FAILURE]: Unable to upload File." )
        except Exception as e:
            Console.stop_loading()
            print("\n\n[ERROR]: Exception occured while uploading Library")
        finally:
            Console.stop_loading()


        time.sleep(2)
        input("press a button to continue ...")


    def download_library(self):
        """
        *****************************************
        Download Library command

        *****************************************
        """
        Console.app_title()
        Console.menu_title("Download Library")

        # View All Library
        dirs =  Auxiliaries.scan_dir(Config.LIBS_DIR)
        options = dict()
        n =1

        for dir in dirs:
            options[n] = dir
            print("{} - {} ".format(str(n), dir))
            n += 1

        print("\n\n Enter <exit> to quit \n\n")

        # Choose an option
        choice =""
        while True :
            choice = input("Enter an option : ")
            if choice.upper() == "EXIT":
                return
            elif Auxiliaries.isInteger(choice) is False:
                print("Invalid Option Provided. ")
            elif int(choice) in options.keys():
                break
            else:
                print("Invalid Option Provided. ")

        library_id = str(options[int(choice)]).replace(".lib", "")

        # Push to queue
        if Config.add_pending_download_lib(library_id) is True:
            print("Library id {} has been successfully loaded".format(library_id))
            time.sleep(2)
            self.view_downloads()

        else:
            print("Sorry, failed to load Library id {}")

        print(Config.LIST_PENDING_LIB)


    def view_downloads(self):
        """
        *****************************************
        View Log

        *****************************************
        """
        prev_combined = ""
        Stuff_metadata = dict
        while True:

            # Load All the Stuff Being download
            list_of_downloads = Config.LIST_IN_PROGRESS_LIB + Config.LIST_PENDING_LIB


            # Get Informations about their library if not exist


            combined = "\nPENDING DOWNLOAD\n--> {}\n\nDOWNLOAD IN PROGRESS\n--> {}\n\nDOWNLOADED\n--> {} \n\n\n\n".format(str(Config.LIST_PENDING_LIB), str(Config.LIST_IN_PROGRESS_LIB), str(Config.LIST_DOWNLOADED_LIB))

            if prev_combined != combined:
                Console.app_title()
                Console.menu_title("View Downloads")
                print("{}\n\n  Press <Enter> to quit log ...".format(combined))
                if Auxiliaries.input_timeout(1) == "":
                    break
                prev_combined = combined
            else:
                if Auxiliaries.input_timeout(2) == "":
                    break

    def view_log(self):
        """
        *****************************************
        View Log

        *****************************************
        """

        prev_combined = ""
        while True :
            combined = ""
            for line in Auxiliaries.LOG_BUFFER:
                combined += "\n"+str(line[0])

            if prev_combined != combined:
                Console.clear_screen()
                print("{}\n\n  Press <Enter> to quit log ...".format(combined))
                if Auxiliaries.input_timeout(5) == "":
                    break
                prev_combined = combined
            else:
                if Auxiliaries.input_timeout(5) == "":
                    break

    def view_services(self):
        """
        *****************************************
        View Log

        *****************************************
        """
        prev_combined = ""

        while True:
            distributor_status = "OFF"
            requestor_status = "OFF"

            if Distributor.get_service_status() is True:
                distributor_status = "RUNNING"
            if Requestor.get_service_status() is True:
                requestor_status = "RUNNING"

            combined = "Distributor service ( {} )\n\nRequestor Service ( {} ) \n\n\n".format(distributor_status,requestor_status)

            if prev_combined != combined:
                Console.app_title()
                Console.menu_title("Services")
                print("{}\n\n  Press <Enter> to quit log ...".format(combined))
                if Auxiliaries.input_timeout(5) == "":
                    break
                prev_combined = combined
            else:
                if Auxiliaries.input_timeout(5) == "":
                    break

    def settings(self):
        """
        *****************************************
        Setting menu

        *****************************************
        """
        Console.app_title()
        Console.menu_title("Settings")

        all_config_vars = dict(Config.view_global_var())
        for key  in all_config_vars:
            print("[ {} ] = {} ".format(str(key), all_config_vars[str(key)]))

        print("\n Enter <exit> to quit \n")

        while True:
            choice = input("Enter key to modify: ")
            choice = choice.strip().upper()

            if choice == "EXIT":
                return

            elif choice not in all_config_vars.keys() :
                print("Unknown key [ {} ] provided.".format(choice))

            elif choice == "" :
                print("No option provided")

            elif choice in all_config_vars.keys() :
                value = input("Provide new value  for [{}]: ".format(choice))
                value = value.strip().upper()
                if value == "EXIT":
                    return self.settings()
                else:
                    Console.start_loading("Updating Config")
                    status, msg = Config.update_global_var(choice, value)
                    time.sleep(2)
                    Console.stop_loading()
                    if status is True:
                        print("[ SUCCESS ] - Config successfully set ")
                        time.sleep(3)
                    else:
                        print("[ FAILURE ] - {}".format(msg))
                        Auxiliaries.input_timeout(5)
                    return self.settings()
            else:
                print("Unknown key [ {} ] provided.".format(choice))

    def about(self):
        """
        *****************************************
        View Log

        *****************************************
        """
        Console.app_title()
        Console.menu_title("About")

        message = "EMMA Torrent V1.0 \nUniversity Jean Monnet \nGroup I\n"
        print("{}\n\n  Press <Enter> to quit log ...".format(message))
        Auxiliaries.input_timeout(15)



    def exit_menu(self):
        """
        *****************************************
        Exit Menu

        *****************************************
        """
        message = " EMMA Torrent V1.0 \nUniversity Jean Monnet \nGroup I "
        print("\r")
        answer = True
        while answer:
            answer = input("Do you really want to exit EMMA Torrent? : [y|n] ")
            if answer.upper() == "Y":
                Console.start_loading("Exiting")
                Config.persist_setting()
                time.sleep(2)
                Console.stop_loading()
                Console.clear_screen()
                os._exit(0)
            elif answer.upper() == "N":
                return
            else:
                print("Invalid input provided.")

    @staticmethod
    def clear_screen():
        """
        *****************************************
        Clear screen

        *****************************************
        """
        if Auxiliaries.get_os_name() == "WINDOWS":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def app_title():
        """
        *****************************************
        Show app Menu

        *****************************************
        """
        Console.clear_screen()
        print(" --------------------------- ")
        print("|       EMMA TORRENT        |")
        print(" ---------------------------\n\n ")



    @staticmethod
    def menu_title(menu):
        """
        *****************************************
        Clear screen

        *****************************************
        """
        print("\n--[ {} ]--\n\n".format(str(menu).upper()))


    @staticmethod
    def start_loading(message):
        """
        *****************************************
        Loading  screen

        *****************************************
        """
        if Console.LOADING_FLAG is True:
            Console.stop_loading()

        def handle() :
            Console.LOADING_FLAG = True
            LOADING_SHOT = ["|", "/", "-", "\\"]
            i = 0
            while Console.LOADING_FLAG is True :
                sys.stdout.write("\r{} ( {} )".format(message,LOADING_SHOT[i]))
                i += 1
                if i%len(LOADING_SHOT) == 0:
                    i = 0
                time.sleep(0.3)
            sys.stdout.write("\r\r")
        t = Thread(target=handle, args=[])
        t.start()

    @staticmethod
    def stop_loading():
        """
        *****************************************
        Stop Loading  screen

        *****************************************
        """
        Console.LOADING_FLAG = False
        time.sleep(0.5)

    @staticmethod
    def progressbar(current, total, prefix="", size=60, file=sys.stdout):
        """
        *****************************************
        Display a  single progress bar

        :param current: Integer
        :param total: Integer
        :param prefix: String
        :param size: Integer
        :param file: <sys.stdout>
        :return: void
        *****************************************
        """
        count = total

        def show(j):
            x = int(size * j / count)
            file.write("%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count))
            file.flush()

        show(0)
        show(current)
        file.write("\n")
        file.flush()

    @staticmethod
    def show_multiple_progressbar(downloads_meta, size=60):
        """
        *****************************************
        Display a collection of progress bar

        :param downloads_meta: List of List
                [ ["computing", 10, 20], ... ]
        :param size: Integer
        *****************************************
        """
        for meta in downloads_meta:
            Console.progressbar(int(meta[1]), int(meta[2]), meta[0], size)


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
    cli.start_loading("Loading")
    time.sleep(10)
    cli.stop_loading()
    #time.sleep(2)
    print("done sleeping")
    time.sleep(5)