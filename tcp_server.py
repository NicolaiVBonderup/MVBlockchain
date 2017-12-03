#!/usr/bin/python

import socket  
import signal  
import transaction as ts
import block
import blockchain
import pickle

class Server:


    def __init__(self, port = 80):
     
        self.host = ''   # <-- works on all avaivable network interfaces
        self.port = port
        self.chain = blockchain.Blockchain()

    def activate_server(self):
        signal.signal(signal.SIGINT, graceful_shutdown)

        print ("Starting web server")
        s = Server(80)  # Constructs server object
     
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: # user provided in the __init__() port may be unavaivable
            print("Launching HTTP server on ", self.host, ":",self.port)
            self.socket.bind((self.host, self.port))

        except Exception as e:
            print ("Warning: Could not acquire port:",self.port,"\n")
            print ("Attempting to register on higher port.")
            
            user_port = self.port
            self.port = 8080

            try:
                print("Launching HTTP server on ", self.host, ":",self.port)
                self.socket.bind((self.host, self.port))

            except Exception as e:
                print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
                print("Try running the Server in a privileged user mode.")
                self.shutdown()
                import sys
                sys.exit(1)

        print ("Server successfully acquired the socket with port: ", self.port)
        print ("Press Ctrl+C to shut down the server and exit.")
        self._wait_for_connections()

    def shutdown(self):
     
        try:
            print("Shutting down the server")
            s.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            print("Warning: could not shut down the socket. Maybe it was already closed?",e)

    def _gen_headers(self,  code):
     
        h = ''
        if (code == 200):
           h = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
           h = 'HTTP/1.1 404 Not Found\n'

        return h

    def _wait_for_connections(self):
     
        while True:
            print ("Awaiting New connection")
            self.socket.listen(3)

            conn, addr = self.socket.accept()

            print("Got connection from:", addr)

            data = conn.recv(1024)
            string = bytes.decode(data)

            split_message = string.split(' ')
            
            type = split_message[0]
            print (type)
            
            if type is 't':
                type, sender, receiver, message = split_message
                print ("Sender: " + sender + " - Receiver: " + receiver + " - Message: " + message)
                transaction = ts.Transaction(sender,receiver,message)
                b1 = block.Block()
                b1.add_transaction(transaction)
                serial = pickle.dumps(b1)
                print (serial)
                deserial = pickle.loads(serial)
                print (deserial)
            if type is 'b':
                type, message = split_message
                self.blockchain.add_block_to_ledger()
            
            
            
def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() # Shuts down the server
    import sys
    sys.exit(1)
