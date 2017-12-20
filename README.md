### Completion & Defects

Currently, the system is capable of connecting via TCP/IP through sockets, obtaining transactions from clients, sharing contact information with other peers, as well as mining.

Due to difficulties with certain parts of the system, we did not reach full completion of the system. Currently, when a block is mined, it is not properly broadcast throughout the system to other peers, such that they add them to their own chains. Furthermore we did manage to create a p2p Docker setup, but unfortunately we didn't have the time to properly combine the two parts.

### Execution

To run the whole system easily, execute the `run_all.sh` script. This will open four servers, as well as a client for communicating with them.

`run_client_search_ports.sh` will open a client that searches on a range of ports to find available peers. This is not recommended as it takes a long time to complete this process. 

### Example of execution

To test the Blockchain system locally, you will need a Python 3.6 runtime environment [Download Python Here](https://www.python.org/downloads/). When Python is installed you will then need to run the `run_all.sh`. Then in client window you will have to input a name, then a name with who you want to transfer to and then how much you want to transfer. When there have been transfers between 4 to 8 times, one of the server will mine transactions and display a block.

Here you see the 5 windows opened when `run_all.sh` have been executed:

![Imgur](https://i.imgur.com/kM04NzL.png)

*Client view_1: Here you see input in the client terminal to the Blockchain system while its is running.*

![Imgur](https://i.imgur.com/a6Bp2lc.png)

*Server terminal view: Here you you see that after 4-8 transactions the server have started a mining process and completed it.* 



### Sources & Dependencies

- https://github.com/davecan/easychain

Used as a reference part for the required parts of a blockchain system.

- https://stuvel.eu/rsa

RSA library used for creating public/private keypairs.



### Link to the Docker p2p repo

https://github.com/tjaydk/BlockchainDocker

**To run:** 

- Download or clone the repository.
- Open your Docker toolbox and navigate to folder.
- Run the Bash script ` run.sh`. This will build the Docker image and create 4 containers, and afterwards close them down as this was where the actual Blockchain part should have been running. At this point it only generates a user id, and searches for other online users via HTTP.



![Imgur](https://i.imgur.com/3HqNTYr.jpg)

*The Docker uses a web API and communicates over HTTP. Above is a screenshot from the client UI*
