########################################################################################################################
# @ Module : Maestro Service
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : March 2019
# @ Desc   : This Module is the master service that ensures that all  other Sub-Services ( Requestor, Distributor)
#               are perfectly working
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
import time
from threading import Thread
from app.utilites.auxiliaries import Auxiliaries
from app.services.requestor import Requestor
from app.services.distributor import  Distributor


class Maestro:
    ####################################################################################################################
    #                                          MAESTRO MODULE
    ####################################################################################################################

    status = False
    sub_services_pool = ["Distributor", "Requestor"]
    last_message = ""

    def __init__(self):
        """
        *****************************************
        Default Constructor

        *****************************************
        """
        pass

    @staticmethod
    def start_service():
        if Maestro.get_service_status() is True:
            return True

        return Maestro.master_job().start()

    @staticmethod
    def master_job():
        Auxiliaries.console_log("Starting Distributor Server ...")

        def handle():
            try:
                Auxiliaries.console_log("Maestro Server Started")
                Maestro.status = True

                while True:
                    default_sleeping_duration = 14
                    up_flag = True
                    try:
                        for service in Maestro.get_sub_services_pool():
                            service_class = eval(service)

                            # In case service is OFF Try to restart service
                            if service_class.get_service_status() is False:
                                    up_flag = False
                                    Maestro.last_message = "Maestro is attempting to restart service ... [{}] ".format(service)
                                    Auxiliaries.console_log(Maestro.last_message )
                                    service_class.start_service()
                                    time.sleep(1)
                                    # Set an shorter sleeping duration
                                    default_sleeping_duration = 3

                        if up_flag is True:
                            Maestro.last_message = " All sub-services are Running ... ".format(service)
                            Auxiliaries.console_log(Maestro.last_message)

                    except Exception as e:
                        Auxiliaries.console_log("Exception in Maestro :{}".format(e))

                    # Waiting before running another cycle ...
                    time.sleep(default_sleeping_duration)

            except Exception as e:
                Auxiliaries.console_log("Exception in Maestro :{}".format(e))
            finally:
                Maestro.status = False

        t = Thread(target=handle, args=[])
        return t

    @staticmethod
    def get_service_status():
        return Maestro.status

    @staticmethod
    def get_sub_services_pool():
        return Maestro.sub_services_pool

    @staticmethod
    def get_last_message():
        return Maestro.last_message

    ####################################################################################################################
    #                                        END MAESTRO MODULE
    ####################################################################################################################

