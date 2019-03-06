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
import time
import os
import json
from pathlib import Path
from threading import Thread
from app.core.srcpeer import SrcPeer
from app.core.tracker import Tracker
from app.settings.config import Config
from app.librarifier.stuff import Stuff
from app.utilites.security import Security
from app.utilites.auxiliaries import Auxiliaries
from app.services.distributor import Distributor


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
        Auxiliaries.console_log("Starting Requestor service ...")
        if Requestor.service_status is True:
            return True

        Requestor.handle_request_all().start()

    @staticmethod
    def handle_request_all():
        def handle():
            try:
                Auxiliaries.console_log("Requestor service started")

                limit_no_concurrent_lib_jobs = 10
                start_flag = False 

                while True:

                    Requestor.service_status = True
                    # Fetching list of all pending libraries to download ( and push in Library Queue  ) ...
                    # Is there any new libraries  ?
                    if start_flag is False :
                        Requestor.library_queue = Config.LIST_IN_PROGRESS_LIB+ Config.LIST_PENDING_LIB
                        start_flag = True
                    else:
                        Requestor.library_queue =  Config.LIST_PENDING_LIB

                    if len(Requestor.library_queue) > 0:
                        Auxiliaries.console_log("pending downloads detected.", Requestor.library_queue)
                    else:
                        Auxiliaries.console_log("no pending download detected.")

                    # For each library fetching the list of available candidates on their respective tracker
                    for library_id in list(set(Requestor.library_queue)):
                        if Requestor.no_library_jobs >= limit_no_concurrent_lib_jobs:
                            Auxiliaries.console_log("max number of concurrent lib  jobs reached ...", limit_no_concurrent_lib_jobs)
                            break

                        # Creating a Job for every library ...
                        Requestor.library_job(library_id).start()
                        Requestor.library_queue.remove(library_id)

                        if library_id in Config.LIST_PENDING_LIB:
                            Config.remove_pending_download_lib(library_id)
                            if library_id not in Config.LIST_IN_PROGRESS_LIB:
                                Config.add_in_progress_download_lib(library_id)

                    # Sleeping for a while before checking if there is any other pending books that can be processed ...
                    Auxiliaries.console_log("Requestor Service Sleeping ...")
                    time.sleep(20)
                    Auxiliaries.console_log("\nRequestor  Service awaking... active Library {} ".format(Requestor.no_library_jobs))

            except Exception as e:
                Auxiliaries.console_log("Exception {} ".format(e))
            finally:
                Requestor.service_status = False
                Auxiliaries.console_log("Requestor service off")

        t = Thread(target=handle, args=[])
        return t

    @staticmethod
    def get_pending_libraries():
        return Config.LIST_PENDING_LIB

    @staticmethod
    def get_library_obj( library_id ):
        if library_id in Requestor.library_details:
            return Requestor.library_details[library_id]

    @staticmethod
    def get_service_status():
            return Requestor.service_status

    @staticmethod
    def library_job(_library_id): # Manages all request on a particular library

        def handle(library_id):

            Auxiliaries.console_log("starting new library job ....", library_id)
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
            collecting_cycle_limit = 3
            collecting_cycle_counter = 0
            # ---------

            # Loading details about pending library ( Tracker IP and Port,  missing books )...
            Auxiliaries.console_log("libpath".format(library_path))

            library_file = Path(library_path)
            if library_file.exists():
                with open(library_path, 'r') as library_file:
                    document = ""
                    for line in library_file:
                        document = document + str(line)

                    Auxiliaries.console_log("loading library ...", library_id)
                    library_object = json.loads(document)
                    library_checksums = library_object['hashes']

                    # Loading / Creating  stuff ...
                    Auxiliaries.console_log("loading/Creating Stuff ...", library_id)
                    sfuff_file = Path(stuff_file_path)
                    if sfuff_file.exists():
                        stuff_object = Stuff.load(stuff_file_path)
                    else:
                        no_books = len(library_object['hashes'])
                        stuff_object = Stuff(total_no_books= no_books)
                        stuff_object.persist(stuff_file_path)

                if library_object is None:
                    Auxiliaries.console_log("Library file could not be decoded", library_id)
                    preprocess_flag = False

            else:
                Auxiliaries.console_log("Library file not Found", library_id)
                preprocess_flag = False

            library_job_status = preprocess_flag

            # Creating a library Job ...
            while library_job_status:
                try:
                    # Connecting to the Tracker and sending request
                    Auxiliaries.console_log("Connecting to hub", library_id)
                    hub_address = str(library_object["hub_address"]).split(":")
                    tracker = Tracker(Config.HUB_IP, Config.HUB_PORT)

                    res_code, res_data_length, res_data = tracker.list_peers(library_id)

                    # In case < list player > was successful ....
                    if res_code == "200":
                        Auxiliaries.console_log(res_data)
                        list_of_peers = json.loads(res_data)
                        # Register self Distributor on Hub
                        if self_hub_registration_flag is False:
                            Auxiliaries.console_log("Registering current player on hub", library_id)
                            Auxiliaries.console_log("Distributor port" , Distributor.get_port())
                            # Use the real port instead of the hardcoded one
                            if tracker.register_peer(library_id, Distributor.get_ip(), Distributor.get_port()) is True:
                                Auxiliaries.console_log("successfully registered on  hub")
                                self_hub_registration_flag = True

                        my_player_id = Distributor.get_ip() + ":" + str(Distributor.get_port())
                        # Building pool of candidate players ( <str,srcPeers> ) ...
                        for player in list_of_peers:
                            player_parts = str(player).split(":")
                            player_id = player_parts[0]+":" + player_parts[1]

                            if player_id not in player_pool:
                                if player_id != my_player_id:
                                    player_pool[player_id] = SrcPeer(player_parts[0], player_parts[1])
                                    player_pool[player_id].download_job(library_id, collected_books, stuff_object, library_object).start()
                                else:
                                    Auxiliaries.console_log("same player_id", player_id)

                        Auxiliaries.console_log("player_pool", player_pool)

                        # Monitoring  the peers activity until no more books in available from SrcPeer ...
                        while len(player_pool) > 0:
                            try:
                                collecting_cycle_counter += 1
                                # Monitoring all players Activities ...
                                Auxiliaries.console_log("monitoring players activity  ...")
                                player_blacklist = []

                                for player_id in player_pool:
                                    Auxiliaries.console_log("monitoring activity of player_id ", player_id)
                                    if player_pool[player_id].get_activity_status() is False:
                                        player_blacklist.append(player_id)

                                # Collecting all buffered books, check their validity against signature .. .
                                Auxiliaries.console_log("collected_books_to_flush", collected_books)

                                if len(collected_books) > 0 and collecting_cycle_counter > collecting_cycle_limit:
                                    collecting_cycle_counter = 0
                                    len_collected_books = len(collected_books)
                                    for i in range(len_collected_books):
                                        cur_book = collected_books[0]
                                        Auxiliaries.console_log("cur_book", cur_book)
                                        collected_books.remove(cur_book)

                                        # Checking  the current book against the checksum before adding book(s) to stuff
                                        if Security.sha1(cur_book[1]) == library_checksums[cur_book[0]]:
                                            stuff_object.constructBook(cur_book[1], int(cur_book[0]))
                                        else:
                                            Auxiliaries.console_log("book discarded", Security.sha1(cur_book[1]), library_checksums[cur_book[0]])

                                    # Persisting collected books to disk ...
                                    Auxiliaries.console_log("flushing ...")
                                    stuff_object.persist(stuff_file_path)

                                # Removing Blacklisted Candidate Players from current Pool ...
                                for player_id in player_blacklist:
                                    Auxiliaries.console_log("removing blacklisted player_id from Pool ", player_id)
                                    del(player_pool[player_id])

                                Auxiliaries.console_log("is_complete", stuff_object.list_book_received )
                                # Checking whether stuff has been fully downloaded ...
                                if stuff_object.is_download_complete():
                                    Auxiliaries.console_log("File completely downloaded ")
                                    # Building file to download Repository
                                    download_path = Config.DOWNLOAD_DIR + os.sep + library_object['file_name']
                                    stuff_object.flushToFile(download_path)
                                    library_job_status = False
                                    # Remove library_id among pending  library ...
                                    Config.remove_in_progress_download_lib(library_id)
                                    Config.add_downloaded_lib(library_id)
                                    break

                            except Exception as e:
                                Auxiliaries.console_log("Exception: {} ".format(e))

                            time.sleep(7)
                            # ------ End of Monitoring ------

                    # In case < list player > failed ....
                    else:
                        Auxiliaries.console_log("error while listing peers.")
                        break

                    # In Library is to be stopped, suspend activities on player pool if any ...
                    if library_job_status is False:
                        # Suspend all current candidates peer
                        for player_id in player_pool:
                            # player_pool[player_id]
                            player_pool[player_id].set_activity_status(False)

                    time.sleep(20)  # Seconds
                    # ---------  End Library job cycle ----------

                except Exception as e:
                    Auxiliaries.console_log("Exception {}".format( e) )
                    # traceback.print_exc()
                finally:
                    Requestor.no_library_jobs -= 1
                    Auxiliaries.console_log("exiting  library job ....", library_id)

            # ---------  End Library job  ----------
        t = Thread(target=handle, args=[_library_id])
        return t

    ####################################################################################################################
    #                                        END REQUESTOR MODULE
    ####################################################################################################################


