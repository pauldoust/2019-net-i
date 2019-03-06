# EMMA TORRENT PROTOCOL  


- **Version** : 0.1
- **Created on**:  08/02/2019
- **Created by**:  Group I  & Group J  
- **Created at**:  Universite  Jean Monnet ( Computer Networks Class - Master I  ) 


 This document discusses all protocols  needed to integrate to the **EMMA Torrent** over P2P network.
 The **EMMA Torrent**  is essentially composed of the below entities.
 
 > **Player** : Peer(s)/Client(s) on the network that can  request and distribute  book(s) (file chunk)  from/to other peer/client.
 >
 > **Tracker** : Central server that keeps track of all peers (IP and PORT) registered to specifics libraries( metadata of the file to download) and avails those resources on its socket interface  .

 
 
 All The protocols stated below have to be implemented by any Peer/Player wishing to communicate with the Tracker or exchange books/ file chunck
 with other peers/Players over this P2P network. 
   


> ###**FORMATTING**
> 
> All the requests and responses in every protocol follow the below structure/synopsis  
>
> **REQUEST SYNOPSIS**  : 
>
>     [COMMAND] [ARG_1] [ARG_2] ... [ARG_N] \r\n
>
>  > **COMMAND**: The Request Keyword or indentify.  
>  >
>  > **[ARG_1] [ARG_2] ... [ARG_N]**: Set of arguments sent along with the *COMMAND*. 
>
> **RESPONSE SYNOPSIS** 
>   
>     [STATUS_CODE] [RESP_1] [RESP_2] ... [RESP_N] \r\n
>  > **STATUS_CODE**: The response status code .
>  >
>  > **[RESP_1] [RESP_2] ... [RESP_N]**: Set of responses parameters returned along the *STATUS_CODE*.
>  


## Communication between  Player and  Tracker 


This section  discusses all protocols  needed  by a player to communicate with the tracker. 

In each protocol, we describe the **request** format/synopsis as sent by Player, all possible **responses** contents returned by  Tracker , the  **variables** ( enclosed into brackets )  in the request and/or response synopsis  as well as as well sample request(s) and response(s).


> **Note**: The set of characters used to mark the end of all request and response synopsis in the below protocols  will be  "**\r\n**"


##### 1. LIST PEERS 

**LIST PEERS** will be used by a player to request the list of registered players for a  given library.   
  
- **Request**
   
   `LIST_PEERS  [library_id]`
   
   * **library_id**  : *Alphanumeric String* used to uniquely identify a library on the Tracker. It is 14 characters long. 
    
 
- **Response**: 

	`200 [list_of_peers_length] [list_of_peers]`
	
	`300`
		
	`400` 
	
	`401` 
	
	`402` 
	
	`500` 

	 * variables  description
	   
	   * **list_of_peers_length**: *Unsigned 16-bit Integer* that specifies the length/size of the list of peers/Players in bit. It ranges between 0 and 65 535 (Unsigned 16-bit integer). 
	       
       * **list_of_peers**:  *List of JSONObject Encoded String*  representing the list of all players registered to the given library. Each JSON Object contains the Keys **peer_ip** and  **peer_port**  representing respectively the IP and PORT of the Player/peer.  
      
	 * status codes description
	 
	   * **200** : OK / Request Successfully handled
	   * **300** : Tracker Busy 
	   * **400** : Unknown / Invalid   Command 
	   * **401** : Invalid  Command Syntax
	   * **402** : Invalid  Command argument(s) 
	   * **500** : Tracker Sever Error 
	   
	  
	   
 - **Sample request(s) and response(s)** 
    
    
    PeerA :> LIST_PEERS lib00001 \r\n
    
    
    PeerB :> 200 50 [{“peer_ip”:”198.16.16.192”,”peer_port”:”5000” } ] \r\n
    
   ---
    
    PeerA :> LIST_PEERS lib01095 \r\n
    
    
    PeerB :> 500 \r\n
    
    

 ##### 2. REGISTER PEER 

This protocol is used by the Player to register itself on the tracker as a Player for a given library.
A typical scenario will be the first peer registering itself via this Protocol after uploading the library.  


 - **Request**
	  
	  `REGISTER_PEER  [library_id] [peer_ip] [peer_port]`
	  * **library_id**  : *Alphanumeric String* used to uniquely identify a library on the Tracker. It is 14 characters long. 
    
      * **peer_ip**: *String* representing the Sever IP of the Player that initiates the registration process. 
	   
      * **peer_port**:  *Unsigned 16-bit Integer* that specifies the socket server port of  the  Player that initiates the registration process. It ranges between 0 and 65 535 (Unsigned 16-bit integer).  
  
  - **Response** 
	
	`200`
	
	`300`
	
	`400` 
	
	`401` 
	
	`402` 
	 
	`500` 
	
	 * status codes description 
	 
	   * **200** : OK / Player has been successfully registered 
	   * **300** : Tracker Busy 
	   * **400** : Unknown / Invalid   Command 
	   * **401** : Invalid  Command Syntax
	   * **402** : Invalid  Command argument(s)   
	   * **500** : Tracker Sever Error 

 - **Sample request(s) and response(s)** 
    
    
    PeerA :> REGISTER_PEER lib00001 192.68.32.41 5001 \r\n
    
    
    PeerB :> 200 \r\n
    
   ---
    
    PeerA :> REGISTER_PEER lib00001 192.68.32.45 8181 \r\n
    
    
    PeerB :> 300 \r\n



## Communication between  Player A and Player B 


This section describes all  protocols one need to implement on a Player's end in other to interact with other Player(s) on the network. 

In each protocol, we  describe the **request** format/synopsis as sent by Player A , all  possible **responses** contents returned by  Player B , the  **variables** ( enclosed into brackets )  in the request and/or response synopsis  as well as as well as sample request(s) and response(s). 

> **Note**: The set of characters used to mark the end of all request and response synopsis in the below protocols  will be  "**\r\n**"




##### 3. PING 

**PING** protocol is used by Player A  to ensure availability of the  Player B. It is 
used just after socket connection between Player A and Player B  or whenever Player B  delays in responding to Peer A. 
 
 
 - **Request**
 
	 `PING  ` 
 
  - **Response** 
  
	`200`
	
	`300`  
    
    `400` 
	
	`401` 
	
	`402` 
	
	`500` 
	 
	 * status codes description 
	 
	   * **200** : Peer is alive/Available 
	   * **300** : Peer Busy 
	   * **400** : Unknown / Invalid   Command 
	   * **401** : Invalid  Command Syntax
	   * **402** : Invalid  Command argument(s) 
	   * **500** : Peer Server Error 
	  

 
 - **Sample request(s) and response(s)** 
    
    
    PeerA :> PING \r\n
    
    
    PeerB :> 200 \r\n
    
   ---
    
    PeerA :> PING \r\n
    
    
    PeerB :> 300 \r\n

##### 4. REQUEST BOOK
 
 This Protocol is used by *Player A*  to request for a missing *book* (File chunk) from *Player B*. 
 
  
 - **Request**
	 
	`REQUEST_BOOK  [library_id] [book_id] `
 
    * **library_id**  : *Alphanumeric String* used to uniquely identify a library on the Tracker. It is 14 characters long. 
       
    * **book_id:** *Unsigned 32-bit Integer* used as as the index of a book in a given library. It ranges between 0 and 4 294 967 295 (Unsigned 32-bit integer). 

    
 - **Response**  
	
	`200 [requested_book_length] [requested_book] `
	
	`300`
	
	`400` 
	
	`401` 
	
	`402` 
	 
	`500` 
	 
	`600`
	
	 * variables  description
	   
	   * **requested_book_length**: *Unsigned 16-bit Integer* that specifies the length/size of the requested book( file chunk ) in bit. It ranges between 0 and 65 535 (Unsigned 16-bit integer). 
	       
       * **requested_book**:  *Stream of Bytes* with length [requested_book_length] representing the requested book ( file chunk )
       
	 * status codes description
	 
	   * **200** : OK / Request Successfully handled
	   * **300** : Peer Busy 
	   * **400** : Unknown / Invalid   Command 
	   * **401** : Invalid  Command Syntax
	   * **402** : Invalid  Command argument(s) 
	   * **500** : Peer Server Error 
	   * **600** : Chunk / Book Not Available 
	  


 
 - **Sample Request(s) and Response(s)** 
    
    
    
    PeerA :> REQUEST_BOOK lib00001  1024 \r\n
    
    
    PeerB :> 200 40 0111111011110111101111001001010101010101 \r\n
    
   ---
    
     PeerA :> REQUEST_BOOK lib00001  1025 \r\n
    
    
    PeerB :> 300 \r\n

##### 5. GET AVAILABLE BOOKS
 
 - **Request**
	
	This request is used to get the list of all available book indexes of a given library  from  Player B. 
	This  could be useful to set emphasis and prioritize the least available books.  
	
	`GET_AVAILABLE_BOOKS  [library_id]`
	
   * **library_id**  : *Alphanumeric String* used to uniquely identify a library on the Tracker. It is 14 characters long.
 
- **Response** 
	
	`200 [length_list_of_available_book] [ids_list_of_available_book]`
		
	`400` 
	
	`401` 
	
	`402` 
	
	`500` 
	
	 * variables  description
	   
	   * **length_list_of_available_book**:   *Unsigned 16-bit Integer* that specifies the length/size of the list of all available books( file chunk ) indexes . It ranges between 0 and 65 535 (Unsigned 16-bit integer).  
	   * **ids_list_of_available_book**: *JSONArray Encoded String*  representing the list of all indexes(0) of available books. This list is not sorted.  

	 * status codes description
	 
	   * **200** : OK / Request Successfully handled
	   * **300** : Peer Busy 
	   * **400** : Unknown / Invalid   Command 
	   * **401** : Invalid  Command Syntax
	   * **402** : Invalid  Command argument(s) 
	   * **500** : Peer Server Error 


 - **Sample request(s) and response(s)** 
    
    
    
    PeerA :> GET_AVAILABLE_BOOKS lib00021 \r\n
    
    
    PeerB :> 200 25 [6,123,89,45,56,98,67,10] \r\n
    
   ---
    
    PeerA :> GET_AVAILABLE_BOOKS lib00021 \r\n
    
    
    PeerB :> 300
    
