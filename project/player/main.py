########################################################################################################################
# @ Module : Main Module
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  loads the client settings and start all the services ( distributor, requestor , collector...)
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################

##################
# @ DEPENDENCIES
##################
from app.services.maestro import Maestro
from app.settings.config import Config
from app.ui.console import Console
import traceback
import os


########################################################################################################################
#                                          MAIN   MODULE
########################################################################################################################

class App:

    @staticmethod
    def start():
        """
        *****************************************
        Method used to start the application
            Ui and services of EMMA Torrents

        :return: Void
        *****************************************
        """
        try:
            # Loading console app in case setup is to be done ...
            cli = Console()
            cli.setup()

            # Loading System Settings ...
            Config.load_setting()

            # Starting Master Service (Maestro)  ...
            Maestro.start_service()

            # Launching Console Application to monitor and manage activities ...
            cli.launch()

        # Handling all exceptions here ...
        except Exception as e:
            from app.utilites.auxiliaries import Auxiliaries
            Auxiliaries.console_log("Exception raised in Main: {} ".format(e))
            traceback.print_exc()


########################################################################################################################
#                                         END MAIN   MODULE
########################################################################################################################


if __name__ == "__main__":
    App.start()

# Review Logging system (done)
# Requestor request book (done)
# Work on Maestro
# Priority Queue
# Remote lib  repo
# Too many IOs in collection reduce the cycle of collection while keeping cycle of blacklist same