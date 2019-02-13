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
from project.player.app.core.srcpeer import SrcPeer
import time
import random
from threading import Thread

##################
# @ GLOBAL
##################
CANDIDATE_PEER_IP = "192.168.43.188"
CANDIDATE_PEER_PORT = 7777

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
        print(peer.get_available_books("lib-0001"))
        peer.disconnect()
        time.sleep(5)

    @staticmethod
    def test_peer_request_books():
        peer = SrcPeer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print(peer.request_book("lib-0001", "book-0001"))
        peer.disconnect()
        time.sleep(5)

    @staticmethod
    def test_list_peers():
        peer = SrcPeer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print("connecting ...")
        print(peer.list_peers("lib00005"))
        peer.disconnect()

    @staticmethod
    def test_register_peer(port_end):
        peer = SrcPeer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print("connecting ...")
        print(peer.register_peer("lib00005","192.168.43.142", "99{}".format(port_end)))
        peer.disconnect()

    ####################################################################################################################
    #                                         END UNIT_TEST MODULE
    ####################################################################################################################


if __name__ == "__main__":
        #UnitTest.test_peer_ping()
        #UnitTest.test_peer_get_available_books()
        #UnitTest.test_peer_request_books()
        UnitTest.test_list_peers()

       # t = Thread()
       # for i in range(1,1000):
       #   t = Thread(target=UnitTest.test_register_peer(i))
       #    t.run()

        # requestor
        # distributor
        # queue
