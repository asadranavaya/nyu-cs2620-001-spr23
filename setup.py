import constants
import node
import os.path
import csv
import socket
import threading
from pythonping import ping

#check validity
if(not os.path.exists(constants.NODE_LOCATION) or not os.path.isfile(constants.NODE_LOCATION)):
    raise FileNotFoundError(constants.NODE_LOCATION_NOT_FOUND)
#read in locations and update the data structures
node_dict = {};

with open(constants.NODE_LOCATION, newline='') as csvfile:
    nodeReader = csv.reader(csvfile, delimiter=",")
    next(nodeReader, None) #skip the headers
    for row_as_node in nodeReader:
        temp_node = node.Node(row_as_node[0], row_as_node[1], row_as_node[2], row_as_node[3])
        node_dict[temp_node.unique_name] = temp_node

# 1. Set up a tcp connection with all nodes
# 2. Notify all nodes of current IP address
# 3. Accept changes of other nodes IP addresses
# 4. Tell other nodes to start
#   4.a. Only start when all nodes have reached consensus

#Set up a client daemon that will continuously send to all nodes an ack to start sending pings
#Will also advertise its IP
sending_socket = socket.socket()
myHostName = socket.gethostname()
recieving_socket = socket.socket()
ipAddress = socket.gethostbyname(myHostName)
port = 7879 #reserve port 7879


def send_and_advertise():
    while True:
        for key, n in node_dict.items(): #Go through each node and advertise
            if n.has_recieved_initial_ack == True:
                continue
            # Else send information 
            host = n.last_reachable_ipv4
            sending_socket.connect((host, port))
            message = constants.START_SENDING +","+ ipAddress + "," + n.unique_name
            message = message.encode()
            sending_socket.send(message)
            data = sending_socket.recv(1024).decode() #recieve response
            if(data == constants.INITIAL_RESPONSE_ACK_GOOD):
                n.has_recieved_initial_ack = True

            
background_sending_thread = threading.Thread(target=send_and_advertise)
background_sending_thread.daemon = True
background_sending_thread.start()

#Recieve any updates from other threads
#recieving_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
recieving_socket.bind((myHostName, port))
recieving_socket.listen(len(node_dict)) #recieve as many connections as nodes in system
recieved_ack_from_nodes_dict = {}
while True:
    print('Waiting for a connection!')
    if len(recieved_ack_from_nodes_dict) == len(node_dict):
        break #Start pinging once all nodes agree that sending should start
    connection, address = recieving_socket.accept()
    print("Recieved a connection")
    data = connection.recv(1024).decode() #recieve advertised information
    response = data.split(",") #indicies should be 0 = start sending, 1 = reachable ip, 2 = unique_node_name
    if response[0] == constants.START_SENDING:
        recieved_ack_from_nodes_dict[response[2]] = constants.START_SENDING
        message = constants.INITIAL_RESPONSE_ACK_GOOD
        message = message.encode()
        connection.send(message)
    else:
        message = constants.INITIAL_RESPONSE_ACK_BAD
        message = message.encode()
        connection.send(message)

#All nodes have agreed, start pinging and close daemon

#test a simple ping
for key, n in node_dict.items():
    ping(n.last_reachable_ipv4, verbose=True)
    
