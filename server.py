#startup before every other node starts up
# 1. Determine number of nodes
# 2. will wait to recieve information updates from every node
#       2.a will create a new node_location file
# 3. Once all nodes have been recieved, send file location to every node
#       3.a Wait for ack from all nodes
# 4. Once all nodes ack, send message to start sending ping and wget

import constants
import node
import socket

number_of_nodes = int(input("Input number of nodes in this expirement: "))
minutes_to_run_experiment = float(input("Input time in minutes to run experiment: "))
sending_socket = socket.socket()
sending_socket.bind((socket.gethostbyname(socket.gethostname()), constants.RESERVED_PORT))
list_of_nodes = []
sending_socket.listen(number_of_nodes) #listen for max number of nodes concurrently
for i in range(number_of_nodes): 
    print("Waiting for connection from node: ",i)
    connection, client = sending_socket.accept()
    print('Connection recieved from: ', client)
    node_information = ""
    while True:
        data = connection.recv(1024).decode()
        if not data:
            break
        node_information += data
    print("Node sent information: " + node_information)
    node_information = node_information.split(",")
    temp_node = node.Node(node_information[0], node_information[1], node_information[2], node_information[3])
    list_of_nodes.append(temp_node)
    connection.close()

#Write new node locations into file
n_list_of_nodes = ["{}\n".format(i) for i in list_of_nodes]
with open(constants.NODE_LOCATION, 'w') as fp:
    fp.writelines(n_list_of_nodes)

#Send file of location information to every node

for i in list_of_nodes:
    sending_file_socket = socket.socket()
    sending_file_socket.connect((i.last_reachable_ipv4, constants.RESERVED_PORT))
    print("Sending file to: ", i.last_reachable_ipv4)
    file = open(constants.NODE_LOCATION, "rb")
    send_data = file.read(constants.BUFFER_SIZE)
    while send_data:
        sending_file_socket.send(send_data)
        send_data = file.read(constants.BUFFER_SIZE)
    file.close()
    print("File sent to node, waiting for ack")
    #Wait for ack from node
    data = sending_file_socket.recv(1024).decode()
    if data == constants.INITIAL_RESPONSE_ACK_GOOD:
        sending_file_socket.close()
        print("File recieved by: ", i.last_reachable_ipv4)

#Send message to all nodes to start pinging

for i in list_of_nodes:
    sending_file_socket = socket.socket()
    sending_file_socket.connect((i.last_reachable_ipv4, constants.RESERVED_PORT))
    message = constants.START_SENDING + "," + str(minutes_to_run_experiment)
    sending_file_socket.send(message.encode()) #send the start message
    print("Sent starting message to: ", i.last_reachable_ipv4)
    #Wait for ack from node to tell other nodes
    data = sending_file_socket.recv(1024).decode()
    if data == constants.INITIAL_RESPONSE_ACK_GOOD:
        sending_file_socket.close()

