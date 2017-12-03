# Module containing our Peer-to-Peer functions
import tcp_server as tcp

server = tcp.Server()

server.activate_server()

# TODO:
# Add list of active nodes.
# Add announcement for the network when node is activated, along with its address.
# Add proof of work.
# 