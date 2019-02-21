########################################################################################################################
# @ Module : Requestor Service
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module connects to a limited range of candidate peer in order to request for one/many books
# @ Ref    : UJM | Computer Network Lab
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
from pathlib import Path
from threading import Thread
from project.player.app.core.srcpeer import SrcPeer
from project.player.app.core.tracker import  Tracker
from project.player.app.settings.config import Config
import socket
import random
import time
import os
import json


class Requestor:
    ####################################################################################################################
    #                                          REQUESTOR MODULE
    ####################################################################################################################

    service_status = False

    # Library Queue
    no_library_jobs = 0

    # Library Queue
    library_queue = list()

    # Library Book Priority Queue
    library_book_queue = dict()

    # Library Book Priority Queue
    library_details = dict()

    def __init__(self):
        """
        *****************************************
        Default Constructor

        *****************************************
        """
        pass

    @staticmethod
    def start_service():
        # Enforcing single Process for Requestor service ...
        print("Starting Requestor service ...")
        if Requestor.service_status is True:
            return True

        Requestor.handle_request_all().start()



    @staticmethod
    def handle_request_all():
        def handle():
            print("Requestor service started")
            Requestor.service_status = True
            limit_no_concurrent_lib_jobs = 10
            while True:

                # Fetching list of all pending libraries to download ( and push in Library Queue  ) ...
                # Is there any new libraries  ?
                Requestor.library_queue = Requestor.get_pending_libraries()
                if len(Requestor.library_queue) > 0:
                    print("pending downloads detected.", Requestor.library_queue)
                else:
                    print("no pending download detected.")

                # For each library fetching the list of available candidates on their respective  tracker ( Library Job inside  )
                for library_id in list(set(Requestor.library_queue)):
                    if Requestor.no_library_jobs >= limit_no_concurrent_lib_jobs:
                        print("max number of concurrent lib  jobs reached ...", limit_no_concurrent_lib_jobs)
                        break

                    # Creating a Job for every library ...
                    Requestor.library_job(library_id).start()
                    Requestor.library_queue.remove(library_id)

                print("Requestor Service Sleeping ...")
                time.sleep(20) #Seconds
                print("\nRequestor  Service awaking...")


            Requestor.service_status = False
            print("Requestor service off")
        t = Thread(target=handle, args=[])
        return t


    @staticmethod
    def get_pending_libraries():
        return Config.LIST_PENDING_LIB



    @staticmethod
    def get_library_obj( library_id ):
        if library_id in Requestor.library_details:
            return Requestor.library_details[library_id]
        pass

    @staticmethod
    def library_job(_library_id): # Manages all request on a particular library

        def handle(library_id):


            preprocess_flag = True
            connected_players = list()
            print("starting new library job ....", library_id)
            Requestor.no_library_jobs += 1

            # Loading details about pending library ( Tracker IP and Port,  missing books )...
            library_path = Config.LIBS_DIR+os.sep+library_id+".lib"
            library_object = None
            print("libpath", library_path)

            library_file = Path(library_path)
            if library_file.exists():
                with open(library_path, 'r') as library_file:
                    document = ""
                    for line in library_file:
                        document = document + str(line)

                    print(document)
                    library_object = json.loads(document)

                if library_object is None :
                    print("Library file could not be decoded", library_id)
                    preprocess_flag = False
            else:
                print("Library file not Found", library_id)
                preprocess_flag = False

            # Creating a library Job ...
            while preprocess_flag:
                # Connecting to the Tracker and sending request
                print("Connecting to hub", library_id)
                hub_address =  str(library_object["hub_address"]).split(":")
                tracker = Tracker(hub_address[0], hub_address[1])
                tracker.connect()
                player_pool = dict()
                print("Connected to hub", library_id)
                res_code, res_data_length, res_data = tracker.list_peers(library_id)

                # In case < list player > was successful ....
                if res_code == "200":
                    print(res_data)
                    list_of_peers = json.loads(res_data)

                    # Building pool of candidate players ( <str,srcPeers> ) ...
                    for player in list_of_peers:
                        player_parts = str(player).split(":")
                        player_id = player_parts[0]+":" + player_parts[1]
                        if player_id not in player_pool:
                            player_pool[player_id] = SrcPeer(player_parts[0], player_parts[1])

                    print("player_pool", player_pool)

                    # Monitoring  the peers activity until no more books in available from SrcPeer ...
                    while len(player_pool) > 0:
                        # look
                        print("monitoring players activity  ...")
                        player_blacklist = []

                        # Verifying players' activity ...
                        for player_id in player_pool:
                            print("monitoring activity of player_id ", player_id)
                            # player_pool[player_id]
                            if player_pool[player_id].get_activity_status() is False:
                                player_blacklist.append(player_id)

                        # Reviewing queue distribution ...

                        # Removing Blacklisted Candidate Players from current Pool  ...
                        for player_id in player_blacklist:
                            print("removing blacklisted player_id from Pool ", player_id)
                            del(player_pool[player_id] )

                        time.sleep(20)



                    # Build the Library Book Priority Queue ...
                    # Connect to all Players, ping and perform book discovery ...

                    # Distribute all the batch of books to SrcPeers ( which will notify the Requestor service once done)

                # In case < list player > failed ....
                else:
                    print("error while listing peers")

                time.sleep(20)  # Seconds
                break # Exit from library Job ( this action should be done when library is fully downloaded or we cant connect to hub )

            Requestor.no_library_jobs -= 1
            print("exiting  library job ....", library_id)
        t = Thread(target=handle, args=[_library_id])
        return t



    ####################################################################################################################
    #                                        END REQUESTOR MODULE
    ####################################################################################################################


if __name__ == "__main__":
    Requestor.start_service()

