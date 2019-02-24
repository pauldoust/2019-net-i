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
from app.services.distributor import Distributor
from app.services.requestor import Requestor
import time

########################################################################################################################
#                                          MAIN   MODULE
########################################################################################################################

# Starting Distributor Service
Distributor.start_service(5002)

time.sleep(5)
# Starting Requestor Service
Requestor.start_service()

########################################################################################################################
#                                         END MAIN   MODULE
########################################################################################################################
