"""
DESCRIPTION
    config module provides hub configuration, server
    status codes and custom exceptions.
"""

# --- constants used ---
BACKUP_INTERVAL = 60.  # in seconds - interval between database saves
CODEC = 'utf8'
# TODO: figure out what the heck is the host
HOST = ''  # all available interfaces
MAX_MESSAGE_LENGTH = 2*1024  # maximum message length, bytes
PEER_COUNT = 10  # how many peers will be sampled from database
PORT_NUMBER = 7777
TIMEOUT = 60.  # timeout time for client, in seconds

# end-of-message antics
BEFORE_END_FLAG = b'\r'
END_SYMBOL = b'\n'
MESSAGE_END = BEFORE_END_FLAG + END_SYMBOL


# --- server status codes ---
b_OK = b'200'
#b_BUSY = b'300'
b_INVALID_COMMAND = b'400'
b_INVALID_SYNTAX = b'401'
b_INVALID_ARGUMENTS = b'402'
b_SERVER_ERROR = b'500'

# --- custom errors ---
class InvalidArgumentsError(Exception):
    """Request arguments are invalid."""
    pass
class InvalidCommandError(Exception):
    """The request is not recognized."""
    pass
class InvalidSyntaxError(Exception):
    """Request syntax is invalid."""
    pass