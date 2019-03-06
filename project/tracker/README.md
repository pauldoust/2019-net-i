# Hub 

## Running the hub

Before running the hub, check out *config.py* file's **constants used** section to specify the parameters of the server.
Make sure the PORT is unoccupied.

After that, just execute the *hub.py* file to boot up a server.

## Checking what's going on

While running, the terminal will print some information to the standard output:

* information about received connection
* message received from client's socket
* message when peer is added to the library
* list of peers to send

## Hub Architecture

Hub module has two aims:

* keeping track of available peers 
* handling their requests

It maintains **a database** in order to do so.
On a boot up, hub tries to recover previously saved database; otherwise, initializes empty one.

While running, it **listens** for a connection and allocates **a thread** to deal with further communication. 
Once connection is accepted, the hub

1. receives a message from a peer
2. decodes it into a request
3. based on request, executes correct operation
4. closes the connection

Once in a while **saves** current database in the same folder where it was run.

## Note

For list of supported requests refer to the **protocol.md** file.
