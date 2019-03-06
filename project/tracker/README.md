To bring hub on-line, just run this. To connect, peers must know your IP
and PORT.

**DESCRIPTION**

Hub module keeps track of available peers and handles their requests.
The hub maintains a database to keep track of libraries and corresponding 
lists of peers. On a boot up, hub tries to recover previously saved
database; otherwise, it initializes empty one.

While running, it accepts a connection and allocates a thread to deal with
further communication. Once connection is accepted, hub tries to receive 
a message from a client, decode it into a request and then execute 
the request.

If the request is invalid (valid command, bad arguments, etc.), closes the 
client socket connection, sends back error code and stops the allocated 
thread.

Once in a while the hub makes a backup of its current database.
