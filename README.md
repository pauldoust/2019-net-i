# TODO

# Instructions on how to build, run, and test your project

## Running the hub

Before running the hub, check out *config.py* file's **constants used** section to specify the parameters of the server.
Make sure the PORT is unoccupied.

After that, just execute the *hub.py* file to boot up a server.

# Description of the architecture (what parts interacts how with what other parts)

## Librarifier
Small sub-module used to generate **.libr** meta-file description of an original file.

## Tracker (or hub)
Keeps track of players in a database, handles their requests.

Players connect to the hub using its address and port, then send their reqeusts. Then they get an answer.
