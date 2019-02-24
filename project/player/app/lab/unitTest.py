########################################################################################################################
# @ Module : unitTest
#
# @ Author : EMMA (Group I)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  test all  Claass/Modules key Functionalities
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
from app.core.srcpeer import SrcPeer
import time
import random
from threading import Thread

##################
# @ GLOBAL
##################
from app.core.tracker import Tracker
from app.settings.config import Config
from app.utilites.netutils import Netutils

CANDIDATE_PEER_IP = "127.0.0.1"
CANDIDATE_PEER_PORT = 5002

class UnitTest:
    ####################################################################################################################
    #                                           UNIT_TEST MODULE
    ####################################################################################################################
    def __init__(self):
        pass

    @staticmethod
    def test_peer_ping():
        peer = SrcPeer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print("connecting ...")
        print(peer.ping())
        time.sleep(60)
        peer.disconnect()


    @staticmethod
    def test_peer_get_available_books():
        peer = SrcPeer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        #print(peer.get_available_books("lib_1550883701")
        print(peer.get_available_books("lib_1550924691"))

        peer.disconnect()
        time.sleep(5)

    @staticmethod
    def test_peer_request_books():
        peer = SrcPeer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print(peer.request_book("lib_1550916735", "6"))
        peer.disconnect()
        time.sleep(5)

    @staticmethod
    def test_list_peers():
        tracker = Tracker("198.58.103.254", "7777")
        print("connecting ...")
        print(tracker.list_peers("lib-001"))
        print(tracker.list_peers("lib_1550861917"))

        tracker.disconnect()

    @staticmethod
    def test_register_peer(port_end):
        tracker = Tracker("198.58.103.254", "7777")
        print("connecting ...")
        #print(tracker.register_peer("lib-001","127.0.0.1", "5002"))
        #print(tracker.register_peer("lib_1550924691", "127.0.0.1", "5001"))
        #print(tracker.register_peer("lib_1550924691", "127.0.0.1", "5002"))
        #print(tracker.register_peer("lib_1550924691", "127.0.0.1", "5003"))
        #print(tracker.register_peer("lib_1550924691", "127.0.0.1", "5004"))
        print(tracker.register_peer("lib_1550916735", "127.0.0.1", "5002"))

        tracker.disconnect()

    ####################################################################################################################
    #                                         END UNIT_TEST MODULE
    ####################################################################################################################


if __name__ == "__main__":
        #UnitTest.test_peer_ping()
        #UnitTest.test_peer_get_available_books()
        #UnitTest.test_peer_request_books()
        UnitTest.test_register_peer("22")
        #UnitTest.test_list_peers()

       # t = Thread()
       # for i in range(1,1000):
       #   t = Thread(target=UnitTest.test_register_peer(i))
       #    t.run()

        #print( Netutils.get_my_remote_ip() )
        print(Config.LIBS_DIR)

        # requestor
        # distributor
        # queue
        #print(repr(bytearray(list(b"www"))))
        print( Netutils.diff_list(list(range(0,5)), list(range(0,10))))
