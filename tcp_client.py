import socket
import sys
# Using this library to generate public/private keys.
import rsa
import time
import signal

host = "localhost"
port = 8080
USER = ""


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tuple with the public/private keys.
# Using 512 bit encryption because the recommended minimum bit size for SHA256 is 496 bits.
publickey, privatekey = rsa.newkeys(512)

def activate_server():
    
        signal.signal(signal.SIGINT, graceful_shutdown)

        print ("Starting web server")
        USER = input("Input username: ")
        port = 8080
     
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: # user provided in the __init__() port may be unavailable
            print("Launching HTTP server on ", host, ":",port)
            client_socket.bind((host, port))

        except Exception as e:
            print ("Warning: Could not acquire port:",port,"\n")
            print ("Attempting to register on higher port.")
            
            user_port = port
            port = 80

            try:
                print("Launching HTTP server on ", host, ":",port)
                client_socket.bind((host, port))

            except Exception as e:
                print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
                print("Try running the Server in a privileged user mode.")
                shutdown()
                import sys
                sys.exit(1)

        print ("Client successfully acquired the socket with port: ", port)
        print ("Press Ctrl+C to shut down the client and exit.")
        _wait_for_connections()
        
def _wait_for_connections():
        
        while True:
            
            try:
                # Connect to server and send data
                data = get_user_input()
                
                # RSA and TCP requires bytes and not strings, so encoding it.
                message = str(data + "\n").encode('utf-8')
                # Can only be decrypted with the public key.
                encrypted_message = rsa.encrypt(message, privatekey)
                full_message = USER + " " + str(encrypted_message)
                
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
    


activate_server()