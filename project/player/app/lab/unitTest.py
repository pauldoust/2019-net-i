########################################################################################################################
# @ Module : unitTest
#
# @ Author : EMMA (Group J)
# @ Course : Computer Network
# @ Since  : January 2019
# @ Desc   : This Module  test all  Claass/Modules key Functionalities
#
#
########################################################################################################################


##################
# @ DEPENDENCIES
##################
from project.player.app.core.peer import Peer
import time


##################
# @ GLOBAL
##################
CANDIDATE_PEER_IP = "127.0.0.1"
CANDIDATE_PEER_PORT = 5001

class UnitTest:
    ####################################################################################################################
    #                                           UNIT_TEST MODULE
    ####################################################################################################################
    def __init__(self):
        pass

    @staticmethod
    def test_peer_ping():
        peer = Peer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print(peer.ping())
        peer.disconnect()
        time.sleep(5)

    @staticmethod
    def test_peer_get_available_books():
        peer = Peer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print(peer.get_available_books("lib-0001"))
        peer.disconnect()
        time.sleep(5)

    @staticmethod
    def test_peer_request_books():
        peer = Peer(CANDIDATE_PEER_IP, CANDIDATE_PEER_PORT)
        peer.connect()
        print(peer.request_book("lib-0001", "book-0001"))
        peer.disconnect()
        time.sleep(5)

    ####################################################################################################################
    #                                         END UNIT_TEST MODULE
    ####################################################################################################################


if __name__ == "__main__":
        UnitTest.test_peer_ping()
        UnitTest.test_peer_get_available_books()
        UnitTest.test_peer_request_books()
        # requestor
        # distributor
        # queue