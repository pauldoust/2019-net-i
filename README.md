# TODO

# Instructions on how to build, run, and test your project

## Running the hub

Before running the hub, check out *config.py* file's **constants used** section to specify the parameters of the server.
Make sure the PORT is unoccupied.

After that, just execute the *hub.py* file to boot up a server.



## How to Install and  Run <Emma Torrent> Player   


There are no external libraries required to install "EMMA Torrent" Player.  All libraries used are in-built assuming that in the Python versions described below  

Recommended Python Version  3.5+ 
Supported Operating Systems:  Linux, Windows 7+ 


Open your terminal / Command Line Interface 
Browse to the Player folder where the main.py is located 
Execute the below command 

> Python main.py 



The console interface of Player  will initilize the Setup procedure on the first execution.  You will be required to provide the below details 

* *HUB Port* ( Type skip to use default value of remote HUB PORT )
* *HUB IP* ( Type skip to use default value of remote HUB IP )
* *Distributor Port* (Socket Server Port, Type 0 for random port)


Once the setup process completed, your configurations will be saved and the main menu of the console interface will be displayed as show below 

---

 --------------------------- 
|       EMMA TORRENT        |
 ---------------------------

1. Upload File
2. Download File
3. View Download 
4. View Logs 
5. View Services 
6. Settings 
7. About 
8. Exit 


Choose an action: 

---


Note that you can change the settings provided during the setup process  by choosing Menu  6  (Settings) 
 

Let's describe every menu on the interface 

Menu 1: Upload File 
 
	This Option allows a user to upload a file and thus generate a Library file that is sharable to every player. 
	The Generated Player will be in  <PLAYER_FOLDER>/data/libs/lib_<library_id>.lib
	Type "exit" to quit this section 


Menu 2: Download a File 

	This Section allow a user to aquire a file assuming that the  adequated Library file has been manually placed in the 
	library Folder   (<PLAYER_FOLDER>/data/libs)
	Type "exit" to quit this section 


Menu 3: View Download 

	This Menu allow the user to track the Libraries pending download and downloaded so far 


Menu 4: View Logs
	
	This Option allows the user to view all the Events , Service and Debug and Error Logs of the system 

Menu 5: View Services 
	
	"View Services" provides the current states [ RUNNING, OFF ] of the Services of the <Emma Torrent> Player.


Menu 6: Settings 
	
	This option allow a user to view and modify some setting  of the <EMMA Torrent> Player



Menu 7: About  
	
	Display a message about <Emma Torrent> Player


Menu 8: Exit  
	To quit the Application 


# Description of the architecture (what parts interacts how with what other parts)

## Librarifier
Small sub-module used to generate **.lib** meta-file description of an original file.

## Tracker (or hub)
Keeps track of players in a database, handles their requests.

Players connect to the hub using its address and port, then send their reqeusts. Then they get an answer.


## Player 

The Player Module handles exchange of files beteen peers and provide a user interface to  view and manage the files , services  and the system configurations.  

The Emma services is essentially made up three main Services 

	* **Maestro** : Master service that supervised subservices (Requestor, Distributed) states and can attempt to restart them  in case they unexpectely go offline 
	* *Distributor* : Sub service that intializes a socket server and Manages all incoming peers request such as  GET_AVAILABLE_BOOKS, REQUEST BOOK  ... 
	* **Requestor** : Sub service  that loads the library to be downloaded , interract with the hub and request books from candidate peers (peers that have a book of the desired libraries) according to a Priorty Queue Policy. 


