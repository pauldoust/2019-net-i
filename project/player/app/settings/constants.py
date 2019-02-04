import re
from urllib.parse import urlparse, parse_qs
#Tracker Simple text-based protocol:
PROTOCOL_LIST_PEERS = "LIST_PEERS"
PROTOCOL_REGISTER_PEER = "REGISTER_PEER"


PROTOCOL_PARAM_LIB_ID = "libraryid"
PROTOCOL_PARAM_PEER_IP = "peer_ip"
PROTOCOL_PARAM_PEER_SERVER_PORT = "peer_server_port"

#Response Codes:
RESPONSE_CODE_OK = "200"
RESPONSE_CODE_RUNTIME_ERROR = "500"


tests = [
"        'LIST_PEERS'    ?search_query=legend+of+hercules&page=&utm_source=opensearch",
" LIST_PEERS ?libraryid=5",
"LIST_PEERS ?libraryid=5",
"LIST_PEERS ?libraryid=5"]

def parse_protocol(s):
    # return "asdasd", "asdas"
    pattern = re.compile(r"""\s*'(?P<action>.*?)' \s*(?P<qs>.*)""", re.VERBOSE)

    match = pattern.match(s)
    if match:
        action = match.group("action")
        queryString = match.group("qs")
        return action, queryString
    return None, None
        # return (action, queryString)

def parse_parameters(qs):
    # print(parse_qs(urlparse(qs).query))
    return parse_qs(urlparse(qs).query)

def get_parameter(qs, param):
    return parse_parameters(qs)[param][0]

# for test in tests: 
#     print (parse_protocol (test) )



