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

from app.core.distributor import Distributor
from app.core.srcpeer import SrcPeer
from app.core.tracker import  Tracker
from app.librarifier.stuff import Stuff
from app.librarifier.book import Book
from app.settings.config import Config
import socket
import random
import copy
import time
import os
import json

from app.utilites.netutils import Netutils
from app.utilites.security import Security


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
        # TODO: Persisting  list of Pending Lib ...
        return Config.LIST_PENDING_LIB



    @staticmethod
    def get_library_obj( library_id ):
        if library_id in Requestor.library_details:
            return Requestor.library_details[library_id]
        pass

    @staticmethod
    def library_job(_library_id): # Manages all request on a particular library

        def handle(library_id):

            print("starting new library job ....", library_id)
            Requestor.no_library_jobs += 1

            # Shared vars for library Job
            # ---------
            preprocess_flag = True
            library_job_status = True
            player_pool = dict()
            collected_books = []
            stuff_object = None
            library_object = None
            library_checksums = list()
            library_path = Config.LIBS_DIR + os.sep + library_id + ".lib"
            stuff_file_path = Config.STUFFS_DIR + os.sep + library_id + ".pkl"
            self_hub_registration_flag =  False
            # ---------



            # Loading details about pending library ( Tracker IP and Port,  missing books )...
            print("libpath", library_path)

            library_file = Path(library_path)
            if library_file.exists():
                with open(library_path, 'r') as library_file:
                    document = ""
                    for line in library_file:
                        document = document + str(line)

                    print(document)
                    library_object = json.loads(document)
                    library_checksums = library_object['hashes']
                    # Loading / Creating  stuff ...

                    sfuff_file = Path(stuff_file_path)
                    if sfuff_file.exists():
                        stuff_object = Stuff.load(stuff_file_path)
                    else:
                        stuff_object = Stuff()
                        no_books = len(library_object['hashes'])
                        stuff_object.createSeedBooks(no_books)
                        stuff_object.persist(stuff_file_path)


                if library_object is None :
                    print("Library file could not be decoded", library_id)
                    preprocess_flag = False

            else:
                print("Library file not Found", library_id)
                preprocess_flag = False

            library_job_status = preprocess_flag

            # Creating a library Job ...
            while library_job_status:
                try:
                    # Connecting to the Tracker and sending request
                    print("Connecting to hub", library_id)
                    hub_address =  str(library_object["hub_address"]).split(":")
                    tracker = Tracker(hub_address[0], hub_address[1])

                    print("Connected to hub", library_id)
                    res_code, res_data_length, res_data = tracker.list_peers(library_id)

                    # In case < list player > was successful ....
                    if res_code == "200":
                        print(res_data)
                        list_of_peers = json.loads(res_data)
                        # Register self Distributor on Hub
                        if self_hub_registration_flag is False:
                            print("Registering current player on hub", library_id)
                            print("Distributor port" , Distributor.get_port())
                            # TODO: Use the real port instead of the hardcoded one
                            if tracker.register_peer(library_id, Distributor.get_ip(), Distributor.get_port()) is True:
                                print("successfully registered on  hub")
                                self_hub_registration_flag = True

                        my_player_id = "127.0.0.1" + ":" + str(Distributor.get_port())
                        # Building pool of candidate players ( <str,srcPeers> ) ...
                        for player in list_of_peers:
                            player_parts = str(player).split(":")
                            player_id = player_parts[0]+":" + player_parts[1]

                            if player_id not in player_pool:
                                if player_id != my_player_id:
                                    player_pool[player_id] = SrcPeer(player_parts[0], player_parts[1])
                                    player_pool[player_id].download_job(library_id, collected_books, stuff_object, library_object).start()
                                else:
                                    print("same player_id", player_id)

                        print("player_pool", player_pool)


                        # Monitoring  the peers activity until no more books in available from SrcPeer ...
                        while len(player_pool) > 0:
                            try:
                                # look
                                print("monitoring players activity  ...")
                                player_blacklist = []

                                # Verifying players' activity ...
                                for player_id in player_pool:
                                    print("monitoring activity of player_id ", player_id)
                                    if player_pool[player_id].get_activity_status() is False:
                                        player_blacklist.append(player_id)

                                # Collecting all buffered books, check their validity against signature and flush them to stuff ...
                                print("collected_books_to_flush", collected_books)

                                if len(collected_books) > 0:

                                    while len(collected_books) > 0:
                                        cur_book = collected_books[0]
                                        print("cur_book", cur_book)
                                        collected_books.remove(cur_book)
                                        # Checking  the current book against the checksum before adding book(s) to stuff
                                        if Security.sha1(cur_book[1]) == library_checksums[cur_book[0]]:
                                            stuff_object.storeBook(cur_book[1], int(cur_book[0]))
                                        else:
                                            print("book discarded", Security.sha1(cur_book[1]) ,library_checksums[cur_book[0]])


                                    # set time of last flush
                                    print("flushing ...")
                                    stuff_object.persist(stuff_file_path)

                                #TODO: Reviewing queue distribution ... ( This process is done at src level)


                                # Removing Blacklisted Candidate Players from current Pool ...
                                for player_id in player_blacklist:
                                    print("removing blacklisted player_id from Pool ", player_id)
                                    del(player_pool[player_id])

                                print("is_complete", stuff_object.list_book_received )
                                # Checking whether stuff has been fully downloaded ...
                                if stuff_object.is_download_complete():
                                    print("File completely downloaded ")
                                    # Building file to download Repository
                                    download_path = Config.DOWNLOAD_DIR + os.sep +library_object['file_name']
                                    stuff_object.flushToFile(download_path)
                                    library_job_status = False
                                    # TODO : Remove library_id among pending  library ...
                                    break

                            except Exception as e:
                                print("Exception: ",e)

                            time.sleep(3)
                            # ------ End of Monitoring ------

                    # In case < list player > failed ....
                    else:
                        print("error while listing peers.")
                        break


                    # In Library is to be stopped, suspend activities on player pool if any ...
                    if library_job_status is False:
                        # Suspend all current candidates peer
                        for player_id in player_pool:
                            # player_pool[player_id]
                            player_pool[player_id].set_activity_status(False)

                    time.sleep(20)  # Seconds
                    # ---------  End Library job cycle ----------
                    #break # Exit from library Job ( this action should be done when library is fully downloaded or we cant connect to hub )
                except Exception as e :
                    print("Exception", e)
                    pass
            Requestor.no_library_jobs -= 1
            print("exiting  library job ....", library_id)
            # ---------  End Library job  ----------
        t = Thread(target=handle, args=[_library_id])
        return t

    ####################################################################################################################
    #                                        END REQUESTOR MODULE
    ####################################################################################################################


if __name__ == "__main__":
    Requestor.start_service()

