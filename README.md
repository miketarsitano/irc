# irc
An Internet Relay Chat written in Python.

## Project Purpose
I created this IRC to gain experience working with sockets and sending data to and from client to server.
The project does work when uploaded to a server and handles multiple clients well. 


## How it works

### Client
The client has a "main" thread to send a request every second to the server to request messages that have not been sent to them yet. It prints the new messages, and then proceeds to request new ones. the request is a json with a `"cmd"` field that contains the value `"request_messages"` and the hwid in a similar fashion. This allows the server to parse the request and figure out if the messages saved have been sent to the client. 

The client also has a second thread with code supplied from a helpful stack overflow post containing a solution to wait for inputs in a non-blocking way. This allows for the client to have a disconnected function to send messages from. the "cmd" field has the value "send_message"
The client sends the messages in a json with a name and message field filled with the respective data.


### Server
The server is a python socket server formed with code from the documentation for socketserver. I modified it to handle the requests in the form of a json.
As explained before it handles the requests that are json format and if they have "cmd" it will handle them if the value is "send_message" or "request_messages"
