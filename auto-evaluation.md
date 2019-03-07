
## Results with our initial objectives

We followed a roadmap which is initialized in very beginning with milestones for each week to fulfil. We have implemented and tested all the features we defined according to the project description. 

**Week 1 (January 21-27):** Project Requirement Review - 
We had meetings during this week to discuss and understand the project clearly. Everyone got the proper understanding about what is going to be implemented in upcoming weeks. 

**Week 2 (January 28- February 4):** Design Phase - 
We managed to come up with first design of system architecture and protocol. We had meetings with our meta-group and negotiate the protocol. We finalized the detailed design of the system.

**Week 3, 4 (February 5 – February 19)** Implementation - 
We had basic working components, tested separately at the end of this phase. 

**Week 5 (February 20- February 27)**  Integrate all and Testing - 
We did testing together and did modifications as necessary. 

**Week 6 (February 28- March 7)** Documentation - 
We had testing and modifications in the last week also. Complete documentation and no pending tasks. 

## What works in Hub

- Threading
- Accepting connections
- Getting and decoding messages into requests
- Based on request, calling the correct procedure
	* Adding peers
	* Sending back samples of peers
- Handling errors
	* Timeouts for clients
	* Junk input
	* Long messages
- Locks seem to work as well

## What does not work in Hub
- Invalid message encoding is not handled
- Correctness of request arguments is not checked
- No graceful exit if server crashes hard
- Probably will fail under heavy loads (locks to blame)


## What works in Player

- Multi-Threading
	* The ability to handle multiple libraries in parallel
	* Downloading from different peers in parallel
	* Uploading for different peers in parallel
- Communicating with the hub
	* Query the hub to find other players
	* Register the peer for specific library
- Loading the library
- Exchanging Books
	* Download books from other players
	* Provides books to other players
- Persisting the current state every interval of time (to continue downloading after disconnecting)
- Books are downloaded in specific order controlled by Priority Queue (which try to download the rarest book first)
- Provides available books information to other players
- Integrity checking (book sha1 is checked before adding)
- Players with errors or sending forged books are discarded automatically from list of peers of the player
- Performance optimization, flushing to hard drive is controlled by a service that runs each interval of time
- All major operations are logged for Troubleshooting


## What does not work in Player
- The player does not complain players with problems to the hub, instead, the player add them to a local black list



## Parts and time spent by each member

Team leader: Etienne EKPO 

| Name | Time Spent (Hours) | Parts |
| ---- | --- |---|
| Aleksei TCYSIN | 40 | Librarifier, Hub |
| Etienne EKPO | 54 | Player, Services, Core module, Console interface|
| Mohammad POUL DOUST | 40 | Stuff and book manager, Player and Tracker Communication|
| Malshani RANCHA GODAGE | 35 | Hub|


# Good dev practices followed
* Committing/pushing somewhat often
* Indentation + PEP8 formatting respected
* Tried to form consistent abstractions
* Tried to encapsulate implementation details
* Various tests and code reviews
* Commenting and documentation
* Error handling
