# Module containing our Peer-to-Peer functions
import tcp_server as tcp

server = tcp.Server()

server.activate_server()

# TODO:
# Add list of active nodes.
# Add announcement for the network when node is activated, along with its address.
# Add proof of work.
# Add transaction values, to allow for properly determining when to mine
# Add block analysis, when new block is announced to network, check if any transactions are actively being mined, if they are, stop mining and remove transactions from the received block
# Might require threading, maybe start with just finishing mining, check if there's any new blocks invalidating afterwards.