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


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tuple with the public/private keys.
# Using 512 bit encryption because the recommended minimum bit size for SHA256 is 496 bits.
publickey, privatekey = rsa.newkeys(512)

def activate_client():
    
    ping_network_for_peers()
    _wait_for_connections()

def ping_network_for_peers():

    if testargs is not " ":
        ports = [int(x) for x in testargs.split(" ")]
    else: 
        ports = range(8000,9000)
    
    book = Phonebook()
    
    for port_in_range in ports:
        
        try:
            print(port_in_range)
            sock.connect((host, port_in_range))
            sock.sendall(bytes('ping', 'utf-8'))
            
            received = str(sock.recv(1024), "utf-8")
            message = received.split(' ')
            
            print (received)
            
            if message[0] is 'ack':
                message_type, peer_UID, peer_port, peer_pubkey = message
                print ('Peer found at port ',peer_port)
                peer_dict = {'UID': peer_UID, 'port': peer_port, 'pubkey': peer_pubkey}
                book.add_peer_to_phonebook(peer_dict)
        
        except Exception as e:
            print (e)
            sock.close()
        finally:
            pass
            sock.close()
            
        
def _wait_for_connections():
        
        while True:
            
            try:
                # Connect to server and send data
                data = get_user_input()
                
                # RSA and TCP requires bytes and not strings, so encoding it.
                message = str(data + "\n").encode('utf-8')
                # Can only be decrypted with the public key.
                encrypted_message = rsa.encrypt(message, privatekey)
                full_message = "t " + USER + " " + str(encrypted_message)
                
                # Temp for testing
                receiving_port = int(input("Which port to send to?: "))
                
                sock.connect((host, receiving_port))
                sock.sendall(bytes(full_message, "utf-8"))

            finally:
                sock.close()

            print("Sent:     {}".format(data))

            
            
def get_user_input():
    
    try:
        receiver = input("Who will you be sending the transaction to?: ")
        # Needs to be encrypted with recipient's public key.
        message = input("Please input a message for the recipient: ")
        value = input("How many fuckcoins do you want to send to {0}?: ".format(receiver))
        transac_fee = str((10 * float(value)) / 100.0)
        timestamp = time.time()
        return " ".join([receiver, message, str(value), transac_fee, str(timestamp)])
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