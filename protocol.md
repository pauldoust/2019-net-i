# Protocol 

## Tracker-side


##### 1. LIST PEERS 

- *Request*:

    `LIST_PEERS  {library_id}`
 
- *Response*: 

	`200  {list_of_peers}`
	  
	`500` 

>**Example of   { library_id }:**    *lib-00001*

>**Example of   { list_of_peers }:**   *[{“peer_ip”:”198.16.16.192”,”peer_port”:”5000” } ]* 



 ##### 2. REGISTER PEER 

  - *Request*:
	  
	  `REGISTER_PEER  {library_id} {peer_ip} {peer_server_port}`
 
  - *Response*: 
	
	`200`
	 
	`500` 

> **Example of   { library_id }:**    *lib-00001*

> **Example of   { peer_ip }:**    *198.50.100.1*

> **Example of   { peer_server_port }:**   *5013* 


## Peer-side:

##### 3. PING 
 
 - *Request*:
 
	 `PING `
 
  - *Response*: 
  
	`200`
	  
	`500` 


##### 4. REQUEST BOOK
 
 - *Request*:
	 
	`REQUEST_BOOK  {library_id} {book_id}`
 
 - *Response*: 
	
	`200  {requested_book} `
	
	`300`
	 
	`500` 
	 
	`600`
	  

> **Example of   { library_id }:**    *lib-00001*

> **Example of   { book_id }:**    *1231*
   

##### 5. GET AVAILABLE BOOKS
 
 - *Request*:
	
	`GET_AVAILABLE_BOOKS  {library_id}`
 
 - *Response*: 
	
	`200 {list_of_available_book_ids}`
	
	`500` 
	  
> **Example of   { library_id }:**    *lib-00001*

> **Example of   { list_of_available_book_ids }:**    *[ 6 , 123, 89 ,45 ,56,  98 , 67 ,10  ]*

## Status Code Description


- **200** : *Integer | OK / Request successfully handled*

- **300** : *Integer | Peer/Player is busy*

- **500** : *Integer | Runtime Error*

- **600** : *Integer | Chunck/Book Not available*