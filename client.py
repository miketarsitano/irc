import socket
import os 
import json
import threading
import time 
import datetime

# Local Imports 
from config import HOST, PORT
from common_funcs import bite, get_hwid


global hwid
hwid = get_hwid()
global username 
username = input("Enter your username: ")


# From https://stackoverflow.com/a/57387909
# This is what will allow me to get keyboard input while also printing new chat messages!
class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return


# From https://stackoverflow.com/a/57387909
# This is what we pass into the KeyboardThread object as what to do with our input.
def my_callback(inp):

    if inp == "disconnect":
        os.exit()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        cmd_dict = {
            "cmd": "send_message",
            "hwid": hwid,
            "content": inp,
            "username": username
        }

        tosend = bite(json.dumps(cmd_dict))

        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(tosend)

        received = str(sock.recv(1024), "utf-8")

# This function just clears the console before the IRC starts.
def render():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    render()

    # From https://stackoverflow.com/a/57387909
    kthread = KeyboardThread(my_callback)


    error_count = 0

    while True:

        """
        THIS WHILE LOOP IS WHERE WE WILL
        REQUEST THE SERVER FOR MESSAGES
        WE HAVE NOT GOTTEN YET.

        WE WILL PRINT NEW MESSAGES WE HAVENT GOTTEN YET.
        """

        time.sleep(1)

        try:


            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                cmd_dict = {
                    "cmd": "request_messages",
                    "hwid": hwid
                }

                tosend = bite(json.dumps(cmd_dict))
                
                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(tosend)

                # Receive data from the server and shut down
                received = str(sock.recv(1024), "utf-8")

                try:
                    data = json.loads(received)
                except:
                    print("Could not decipher data")
                    error_count += 1
                    
                
                for message in data['messages']:

                    # THIS IS WHERE NEW MESSAGES ARE PRINTED
                    dt = datetime.datetime.fromtimestamp(message['time'])
                    mt = dt.strftime("%H:%M:%S")
                    print(f"[{mt}] {message['username']}: {message['content']}")

            

        except ConnectionRefusedError:
            print("Connection Refused.. Server not running.")
            print("-"*10)
            error_count += 1
            
            
        except Exception as e:
            print("Unknown error... \n")
            print(e)
            print("-"*10)
            error_count += 1
            

        if error_count >= 30:
            print("EXITING PROGRAM FOR 30+ ERRORS.")
            print("RESTART AND TRY AGAIN")
            break
        
    

