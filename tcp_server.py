#!/usr/bin/python

import socket  
import signal  
import transaction as ts
import block
import blockchain
import rsa
from phonebook import Phonebook
import sys
import json
from ast import literal_eval
import uuid
from rsa.pkcs1 import VerificationError

class Server:
    
    

    def __init__(self, port = 8080):
    
        self.testargs = " ".join(sys.argv[1:])
        self.publickey, self.privatekey = rsa.newkeys(512)
        self.host = ''   # <-- works on all available network interfaces
        self.port = port
        self.chain = blockchain.Blockchain()
        self.phonebook = Phonebook()
        self.uid = uuid.uuid1()

    def activate_server(self):
        signal.signal(signal.SIGINT, graceful_shutdown)

        print ("Starting web server")
        s = Server(8080)  # Constructs server object
     
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: # user provided in the __init__() port may be unavailable
            print("Launching HTTP server on ", self.host, ":",self.port)
            self.socket.bind((self.host, self.port))

        except Exception as e:
            for i in range (self.port, self.port+1000):
                print ("Warning: Could not acquire port:",self.port,"\n")
                print ("Attempting to register on higher port.")
                
                user_port = self.port
                self.port = self.port+1

                try:
                    print("Launching HTTP server on ", self.host, ":",self.port)
                    self.socket.bind((self.host, self.port))
                    break
                except Exception as e:
                    print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
                    #print("Try running the Server in a privileged user mode.")
                    #self.shutdown()
                    #import sys
                    #sys.exit(1)

        print ("Server successfully acquired the socket with port: ", self.port)
        print ("Press Ctrl+C to shut down the server and exit.")
        self.phonebook.add_peer_to_phonebook(str(self.uid),{'port':str(self.port),'pubkey_e':str(self.publickey.e),'pubkey_n':str(self.publickey.n)})
        if self.port != 8080:
            self.request_phonebook_from_peers()
        self._wait_for_connections()

    def shutdown(self):
     
        try:
            print("Shutting down the server")
            s.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            print("Warning: could not shut down the socket. Maybe it was already closed?",e)

    def request_phonebook_from_peers(self):
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
        # Can add system arguments to the method call if we wanna call just specific ports
        # Mostly used for testing
        if self.testargs != "":
            ports = [int(x) for x in self.testargs.split(" ")]
        else: 
            ports = range(8080,9080)
        
        for port_in_range in ports:
            try:
                sock.connect(('localhost', port_in_range))
                sock.sendall(bytes("book", 'utf-8'))
                    
                received = str(sock.recv(1024), "utf-8")
                message = received.split('$')
                    
                if message[0] == 'bookack':
                    
                    peers_response = json.loads(message[1])
                    clients_response = json.loads(message[2])
                    self.phonebook.update_phonebook(peers_response, clients_response)
            
            except Exception as e:
                pass
                #print (e)
                #sock.close()


    def _wait_for_connections(self):
        # Temp for testing
        b1 = block.Block()
        while True:
            try:
                print ("Awaiting New connection")
                self.socket.listen(3)

                conn, addr = self.socket.accept()

                print("Got connection from:", addr)

                data = conn.recv(1024)
                string = bytes.decode(data)

                split_message = string.split('$?$')
                
                message_type = split_message[0]
                
                if message_type == 'ping':
                
                    message_type, name, pubkey_n, pubkey_e = split_message
                    user_pubkey = {'pubkey_n': int(pubkey_n), 'pubkey_e': int(pubkey_e)}
                    self.phonebook.add_client_to_phonebook(name, user_pubkey)
                
                    ping_response = "ack {0} {1} {2} {3}".format(self.uid,self.port,self.publickey.n,self.publickey.e)
                    conn.send(bytes(ping_response,'utf-8'))
                    
                    
                elif message_type == 't':
                
                    message_type, sender, receiver, message, value, fee, timestamp, verification = split_message
                    
                    verification_message = bytes("$?$".join([receiver, message, str(value), fee, str(timestamp)]),'utf-8')
                    
                    sender_key = self.phonebook.get_pubkey_from_UID(sender)
                    try:
                        if rsa.verify(verification_message, literal_eval(verification), sender_key):
                            
                            print ("Sender: " + sender + " - Receiver: " + receiver + " - Message: " + message)
                            transaction = ts.Transaction(sender,sender,receiver,message)
                            b1.add_transaction(transaction)
                            if b1.has_enough_transactions():
                            #if 1 == 1:
                                b1.mine()
                                self.broadcast_block_to_network(b1)
                                b1.empty_transactions()
                                
                    except VerificationError as e:
                        print ('Not verified')
                        
                        
                elif message_type == 'b':
                    
                    message_type, message = split_message
                    self.chain.add_block_to_ledger(message)
                    
                    
                elif message_type == 'book':
                
                    
                    full_book = self.phonebook.get_all_peers()
                    
                    peers_serialized = json.dumps(full_book[0])
                    clients_serialized = json.dumps(full_book[1])
                    
                    book_response = "bookack$" + peers_serialized + "$" +  clients_serialized
                    
                    
                    conn.send(bytes(book_response,'utf-8'))
                    
                
            finally:
                conn.close()
            
    def broadcast_block_to_network(self, block):
        
        peers = self.phonebook.get_all_peers_for_announcement()
        
        for port_in_range in peers:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                message = "b$?$"+str(json.dumps(block))
                
                sock.connect(('localhost', int(port_in_range)))
                sock.sendall(bytes(message, 'utf-8'))
                
            
            except Exception as e:
                print (e)
                sock.close()
            
            
def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() # Shuts down the server
    import sys
    sys.exit(1)
