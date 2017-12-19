# Module containing our Peer-to-Peer functions
import tcp_server as tcp

server = tcp.Server()

server.activate_server()

# TODO:
# Add block analysis, when new block is announced to network, check if any transactions are actively being mined, if they are, stop mining and remove transactions from the received block
# Might require threading, maybe start with just finishing mining, check if there's any new blocks invalidating afterwards.
# When announcing themselves to the peers, announce with their UID, port, public key and blockchain.
# Make tests to guide development. Easier to figure out what to do when we have a checklist of things that the system should be able to do.
# Define the range of ports we need.
# Figure out the specific UID protocol we want to follow.
# Start server and client at the same time from the main file.
# Refactor the if statements in server to use dictionary mapping
# Make all delimiters the $ sign instead of spaces.