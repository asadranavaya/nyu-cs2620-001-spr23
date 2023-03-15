import constants
import node
import os.path
import csv
import socket
import threading
import requests
from pythonping import ping

def read_node_locations():
    node_dict = {};
    #check validity
    if(not os.path.exists(constants.NODE_LOCATION) or not os.path.isfile(constants.NODE_LOCATION)):
        raise FileNotFoundError(constants.NODE_LOCATION_NOT_FOUND)
    #read in locations and update the data structures

    with open(constants.NODE_LOCATION, newline='') as csvfile:
        nodeReader = csv.reader(csvfile, delimiter=",")
        #next(nodeReader, None) #skip the headers
        for row_as_node in nodeReader:
            temp_node = node.Node(row_as_node[0], row_as_node[1], row_as_node[2], row_as_node[3])
            node_dict[temp_node.unique_name] = temp_node
    return node_dict

# 1. Set up a tcp connection with server
# 2. Notify server of new public IP
# 3. Accept file of other nodes IP addresses
#       3.a Send ack to server about node changes
# 4. Wait for ack to start from server
# 5. Start sending

#Get current IP address
public_ip_response = requests.get(constants.GET_PUBLIC_IP_URL)
current_public_ip = public_ip_response.text

aws_region = input("Input current aws region: ")
#Connect with server
server_socket_connection = socket.socket()
server_socket_connection.connect((constants.SERVER_LOCATION_EC2_EAST, constants.RESERVED_PORT))
print("Sending node information to server at: ", constants.SERVER_LOCATION_EC2_EAST)
self_node = node.Node(constants.AWS_CLOUD, aws_region, current_public_ip, constants.AWS_INSTANCE_T2)
message = self_node.__str__().encode()
print("Sending node information as: ", self_node.__str__())
server_socket_connection.send(message)
server_socket_connection.close()

#recieve new file list of locations from server
recieving_socket = socket.socket()
print("Node is listening on port: ", constants.RESERVED_PORT)
recieving_socket.bind((socket.gethostbyname(socket.gethostname()), constants.RESERVED_PORT))
recieving_socket.listen(1) #at most one server
file = open(constants.NODE_LOCATION, "wb")
while True:
    connection, address = recieving_socket.accept()
    print("Recieving file at: ", constants.NODE_LOCATION)
    recv_data = connection.recv(1024)
    while recv_data:
        file.write(recv_data)
        break
        recv_data = connection.recv(1024)
    file.close()
    print("Node location copied to local disk")
    print("Sending ACK to server")
    connection.send(constants.INITIAL_RESPONSE_ACK_GOOD.encode())
    connection.close()
    break

#Wait for server to say start pinging
while True:
    print("Waiting for server to ack pinging phase")
    connection, address = recieving_socket.accept()
    recv_data = connection.recv(1024).decode()
    if recv_data == constants.START_SENDING:
        connection.send(constants.INITIAL_RESPONSE_ACK_GOOD.encode())
    connection.close()
    print("Server said to start acking")
    break
    
#read in data
node_info_dict = read_node_locations()

#identify which node is self
for key, n in node_info_dict.items():
    if n.last_reachable_ipv4 == current_public_ip:
        n.is_self = True
        print("Found myself")

#Start pinging
for key, n in node_info_dict.items():
   if not n.is_self:
       ping(n.last_reachable_ipv4, verbose=True)

print('Done pinging')

