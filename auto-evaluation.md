# Hub
## What works

- threading
- accepting connections
- getting and decoding messages into requests
- based on request, calling the correct procedure
	* adding peers
	* sending back samples of peers
- handling errors
	* timeouts for clients
	* junk input
	* long messages
- locks seem to work as well

## What does not work
- invalid message encoding is not handled
- correctness of request arguments is not checked
- no graceful exit if server crashes hard
- probably will fail under heavy loads (locks to blame)

## Time spent
Aleksei: 9 hours

# Good dev practices followed
* committing/pushing somewhat often
* indentation + PEP8 formatting respected
* tried to form consistent abstractions
* tried to encapsulate implementation details
* various tests and code reviews
* documentation
* error handling
