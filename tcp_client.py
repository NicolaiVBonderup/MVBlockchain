import socket
import sys
# Using this library to generate public/private keys.
import rsa
import time
import signal
from phonebook import Phonebook

host = "localhost"
port = 8080
USER = input("Input username: ")
testargs = " ".join(sys.argv[1:])
book = Phonebook()


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tuple with the public/private keys.
# Using 512 bit encryption because the recommended minimum bit size for SHA256 is 496 bits.
publickey, privatekey = rsa.newkeys(512)

def activate_client():
    
    ping_network_for_peers()
    _wait_for_connections()

def ping_network_for_peers():

    
    # Can add system arguments to the method call if we wanna call just specific ports
    # Mostly used for testing
    if testargs != "":
        ports = [int(x) for x in testargs.split(" ")]
    else: 
        ports = range(8000,8100)
    
    for port_in_range in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            announcement = "ping$?${0}$?${1}$?${2}".format(USER,publickey.n,publickey.e)
            
            sock.connect((host, port_in_range))
            sock.sendall(bytes(announcement, 'utf-8'))
            
            received = str(sock.recv(1024), "utf-8")
            message = received.split(' ')
            
            if message[0] == 'ack':
                message_type, peer_UID, peer_port, peer_pubkey_n, peer_pubkey_e = message
                peer_pubkey = rsa.PublicKey(int(peer_pubkey_n), int(peer_pubkey_e))
                print ('Peer "{0}" found at port {1}'.format(peer_UID, peer_port))
                peer_dict = {'UID': peer_UID, 'port': peer_port, 'pubkey': peer_pubkey}
                book.add_peer_to_phonebook(peer_UID,peer_dict)
        
        except Exception as e:
            print (e)
            sock.close()
        finally:
            sock.close()
            
    #sock.close()
            
        
def _wait_for_connections():
        
        while True:
        
            # Connect to server and send data
            data = get_user_input()
            
            # RSA and TCP requires bytes and not strings, so encoding it.
            message = str(data).encode('utf-8')
            # Can only be decrypted with the public key.
            #encrypted_message = rsa.encrypt(message, privatekey)
            
            verification = rsa.sign(message, privatekey, 'SHA-1')
            
            full_message = "t$?$" + USER + "$?$" + data + '$?$' + str(verification)
            
            # Temp for testing
            #receiving_port = int(input("Which port to send to?: "))
            
            peers = book.get_all_peers_for_announcement()
            
            for port in peers:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    print (port)
                    sock.connect((host, int(port)))
                    sock.sendall(bytes(full_message, "utf-8"))
                finally:
                    sock.close()

            

            #print("Sent:     {}".format(full_message))

            
            
def get_user_input():
    
    try:
        # Maybe provide a list of known peers?
        receiver = input("Who will you be sending the transaction to?: ")
        # Needs to be encrypted with recipient's public key.
        message = input("Please input a message for the recipient: ")
        value = input("How many coins do you want to send to {0}?: ".format(receiver))
        transac_fee = str((10 * float(value)) / 100.0)
        timestamp = time.time()
        return "$?$".join([receiver, message, str(value), transac_fee, str(timestamp)])
    except Exception as e:
        print ("Input caused an error.")
        print (e)
    
    
def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() # Shuts down the server
    import sys
    sys.exit(1)
    


activate_client()
#_wait_for_connections()