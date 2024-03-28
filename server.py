import socketserver
import time
import json 
import datetime

# Local Imports
from config import HOST, PORT
from common_funcs import bite


global messages
messages = []

class Message():
    def __init__(self, author, name, content, time):
        self.author = author
        self.name = name
        self.content = content
        self.time = time

        self.sent_to = []


# CREDIT TO https://docs.python.org/3/library/socketserver.html
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        

        self.data = self.request.recv(1024).strip()

        try:
            
            data = str(self.data).replace("'", "")
            data = data[1:]
        
            cmd_dict = json.loads(data)
        except Exception as e:

            # I do this to weed out probe requests from interrupting the IRC.
            print(f"ERROR FROM {self.client_address[0]} WITH DATA {str(self.data)}")
            return


        if cmd_dict['cmd'] == "send_message":
            new_message = Message(cmd_dict['hwid'], cmd_dict['username'], cmd_dict['content'], time.time())
            messages.append(new_message)
            self.request.sendall(bite("success"))

            # Printing the message to our console
            dt = datetime.datetime.fromtimestamp(new_message.time)
            mt = dt.strftime("%H:%M:%S")
            print(f"[{mt}] {new_message.name}: {new_message.content}")

            return
        
        elif cmd_dict['cmd'] == "request_messages":

            # We need to get the messages the client hasn't received yet and send them in a list.
            hwid = cmd_dict['hwid']

            messages_to_send = []
            for message in messages:
                if hwid not in message.sent_to:
                    message.sent_to.append(hwid)
                    messages_to_send.append(
                        {
                            "author": message.author,
                            "username": message.name,
                            "content": message.content,
                            "time": message.time
                        }
                    )
            
            self.request.send(bite(json.dumps({"messages": messages_to_send})))


if __name__ == "__main__":


    # This will create the server on HOST:PORT 
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C]
        print("Server Started..")
        server.serve_forever()
        