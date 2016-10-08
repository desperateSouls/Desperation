#!/usr/bin/env python3
__author__ = 'Peter Maar'

import socket
import pickle
import time

SERVER_IP_OR_HOSTNAME = "Ps-Laptop"
#SERVER_IP_OR_HOSTNAME = "10.105.244.179"
TCP_PORT = 10000
BUFFER_SIZE = 1024


# Pickle a variable
def pickleify(variableToPickle):
    pickledMessageTuple = pickle.dumps(variableToPickle, protocol=pickle.HIGHEST_PROTOCOL)
    return pickledMessageTuple

# Unpickle a variable
def unpickle(aPickle):
    unpickled_variable = pickle.loads(aPickle)
    return unpickled_variable

# Create the connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((SERVER_IP_OR_HOSTNAME, TCP_PORT))
except socket.gaierror:
    SERVER_IP_OR_HOSTNAME += ".local"
    s.connect((SERVER_IP_OR_HOSTNAME, TCP_PORT))


# Send an object
def send(objectToSend):
    pickledObjectToSend = pickleify(objectToSend)
    s.send(pickledObjectToSend)


# Recieve an object for 'username'
def recieve(username):
    pickledUsername = pickleify(username)
    s.send(pickledUsername)
    recievedData = s.recv(BUFFER_SIZE)
    unpickledObject = unpickle(recievedData)
    return unpickledObject


# Once done using the network, this should be called to cleanup and close connections
def done():
    s.close()
#
# exampleMessageTuple = (time.time(), "recipient_goes_here", "sender_goes_here", "message_goes_here")
# send(exampleMessageTuple)
#
# print(recieve("username_goes_here"))
#
# done()
