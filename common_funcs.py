
import uuid

from config import FORMAT


# To send data into the common format.
# This just makes it easier since both client and server
# use this function
def bite(string):
    return string.encode(FORMAT)

# To get a unique hardware id for the client user.
def get_hwid():
    return uuid.getnode()

