#!/usr/bin/env python3

import socket
import sys
import pickle
import csv
import os

directory = "data"
if not os.path.exists(directory):
    os.makedirs(directory)

ownHostname = socket.gethostname()
ownIp = socket.gethostbyname(socket.gethostname())
print(ownHostname, ownIp)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ownIp, 10000)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

sock.listen(1)


class StoreThingy:

    def __init__(self, timestamp, sendie, sender, message):
        self.timestamp = timestamp
        self.sendie = sendie
        self.sender = sender
        self.message = message

class Server:
    def save_to_file(dump, serialized):
        sender_data = open("data/" + dump.sender + ".csv", 'w+')
        sender_reader = csv.reader(sender_data)
        sender_writer = csv.writer(sender_data)
        sender_writer.writerow(serialized)
        sendie_data = open("data/" + dump.sendie + ".csv", 'w+')
        sendie_reader = csv.reader(sendie_data)
        sendie_writer = csv.writer(sendie_data)
        sendie_writer.writerow(serialized)


while True:
    # Wait for a connection
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print(sys.stderr, 'connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print(sys.stderr, 'received "%s"' % data)
            if data:

                deserialized = pickle.loads(data, fix_imports=True, encoding="utf-8", errors="strict")
                dump = StoreThingy(deserialized[0], deserialized[1], deserialized[2], deserialized[3])
                serialized = pickle.dumps(dump)

                Server.save_to_file(dump, serialized)
                print(deserialized)
                # for number in deserialized:
                #     print(number)
                #if deserialized == codeword:
                print(sys.stderr, 'sending data back to the client')
                connection.sendall(data)

            else:
                print(sys.stderr, 'no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
