import sys
sys.path.insert(0,'..')

import netutils
from settings.constants import *
# import settings.constants
from server import *
import os
import json
from collections import defaultdict

class Tracker(Server):
    peers = defaultdict(list)

    """docstring for ClassName"""
    def __init__(self, ip= "localhost", port=9999):
        self.peers =  defaultdict(list)

        super(Tracker, self).__init__(ip, port)


    def handler(self, socket):
        def handle2():
            l = netutils.read_line(socket)
            while l is not None:
                action, qs = parse_protocol(l)
                print("ACTION IS: ", action)
                print("Query String is: ", qs)
                parameters = parse_parameters(qs)
                print("params are: ", parameters)
                if action == PROTOCOL_LIST_PEERS:               
                    print("list peers received")
                    library_id = get_parameter(qs, PROTOCOL_PARAM_LIB_ID)
                    print("library_id is ", library_id)
                    res = self.list_peers(library_id)
                    socket.send(res.encode())
                    socket.send(os.linesep.encode())

                    # socket.sendall(RESPONSE_CODE_OK.encode()) 
                elif action == PROTOCOL_REGISTER_PEER:
                    library_id = get_parameter(qs, PROTOCOL_PARAM_LIB_ID)
                    peer_ip = get_parameter(qs, PROTOCOL_PARAM_PEER_IP)
                    peer_server_port = get_parameter(qs, PROTOCOL_PARAM_PEER_SERVER_PORT)
                    res = self.register_peer(library_id, peer_ip, peer_server_port)
                    print(res)

                l = netutils.read_line(socket)
        t = Thread(target=handle2)
        return t

    def list_peers(self, library_id):
        try:
            to_send  = json.dumps(self.peers)
            return to_send
        except Exception as e:
            print("Error: ", e)
            return RESPONSE_CODE_RUNTIME_ERROR

    def register_peer(self, library_id, peer_ip, peer_server_port):
        if not library_id in self.peers:
            self.peers[library_id] = []
            
        self.peers[library_id].append({"peer_ip": peer_ip, "peer_port" : peer_server_port})
        # self.peers[library_id].append({"peer_ip": peer_ip, "peer_port" : peer_server_port})

        return RESPONSE_CODE_OK 

        # try:
        #     self.peers[library_id].append({"peer_ip": peer_ip, "peer_port" : peer_server_port})
        #     return RESPONSE_CODE_OK 

        # except BaseException  as e:
        #     print("Error: ", str(e))
        #     return RESPONSE_CODE_RUNTIME_ERROR



# peers = defaultdict(list)
# def register_peer(library_id, peer_ip, peer_server_port):
#     global peers
#     peers[library_id].append({"peer_ip": peer_ip, "peer_port" : peer_server_port})
#     print(peers)

#     return True 

if __name__== "__main__":
    tracker = Tracker()
    # register_peer("1", "localhost", 2344)
    