"""
DESCRIPTION
    database module provides concise database ADT.

    Database is implemented as a dictionary, with keys being library
    and values being lists of peers.
"""

import copy
import pickle
import random

class Database:
    """ADT representing the database."""

    def __init__(self, input_file='tracker.pickle'):
        """Initializes the database.

        Tries to load the database from input_file. On fail,
        creates empty one.
        """
        
        try:
            # try loading the previously saved database from file
            with open(input_file, "rb") as pickle_in:
                self.db = pickle.load(pickle_in)
        except:
            # if no database is found or smth goes wrong, start with blank one
            self.db = {}

    def __str__(self):
        return str(self.db)

    # --- public methods ---
    def add_peer(self, peer_data, library_id):
        """Adds peer data to the library in a database.

        Takes care of duplicates.
        
        Params:
        ---
        peer_data -- a tuple of (ip:str, port:int) values
        library_id -- string
        """

        # if the library does not exist, create it
        if library_id not in self.db:
            self.db[library_id] = set()

        # add peer info to the library in the database
        # has no effect if a peer is already present
        self.db[library_id].add(peer_data)

    def list_peers(self, library_id, count=10):
        """Returns a list of peers chosen at random.

        Params:
        ---
        library_id -- string
        count -- int (default 10), total count of peers in a list

        Returns:
        ---
        sampled_peers -- list of {'peer_ip': ip, 'peer_port': port} dicts
            If library has less peers than count, will return however many
            peers are available. Returns empty list if library is empty.
        """
        
        # try getting the library list from the database
        result_set = self.db.get(library_id, None)

        # if library is not empty
        if result_set is not None:

            # more than count peers available
            if len(result_set) > count:
                sampled_peers = random.sample(result_set, count)
            # less than count peers available
            else:
                sampled_peers = copy.copy(result_set)

            # change tuples into the dicts to support the protocol
            sampled_peers = [
                {'peer_ip': ip, 'peer_port': port} 
                for ip, port in sampled_peers
                ]

        # on empty library, return empty list
        else:
            sampled_peers = []

        return sampled_peers
        
    def drop(self, library_id):
        """Deletes library form the database (if present)."""

        if library_id in self.db:
            del self.db[library_id]

    def save(self, output_file='tracker.pickle'):
        """Saves database into an output_file using pickle."""

        with open(output_file, "wb") as pickle_out:
            pickle.dump(self.db, pickle_out)