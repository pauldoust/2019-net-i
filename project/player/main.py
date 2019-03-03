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
# Loading Settings params ...
import json

from app.services.distributor import Distributor
from app.services.requestor import Requestor
from app.settings.config import Config
from app.ui.console import Console
#from app.ui.gui import Gui
import time

########################################################################################################################
#                                          MAIN   MODULE
########################################################################################################################

# Loading console app in case setup is to be done ...
cli = Console()
cli.setup()

# Loading System Settings ...
Config.load_setting()


# Starting Distributor Service ...
Distributor.start_service(Config.DISTRIBUTOR_PORT)

# Delaying before proceeding ...
time.sleep(1)

# Starting Requestor Service ...
Requestor.start_service()

# Launching Console Application to monitor and manage activities ...
cli.launch()


########################################################################################################################
#                                         END MAIN   MODULE
########################################################################################################################

# Review Logging system
# Requestor request book
# Priority Queue
# Remote lib  repo