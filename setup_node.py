from pythonping import ping
from time import sleep, time
import constants
import node
import socket
import requests
import helpers
import threading
import wget
import os

# 1. Set up a tcp connection with server
# 2. Notify server of new public IP
# 3. Accept file of other nodes IP addresses
#       3.a Send ack to server about node changes
# 4. Wait for ack to start from server
# 5. Start sending

#Get instance meta-data
cloud_provider = helpers.print_enum_get_response(constants.CLOUD_PROVIDERS)
cloud_region = helpers.print_enum_get_response_as_string(helpers.match_to_region(cloud_provider))
vm_instance = helpers.print_enum_get_response_as_string(helpers.match_to_instance(cloud_provider))

#Get current IP address
public_ip_response = requests.get(constants.GET_PUBLIC_IP_URL)
current_public_ip = public_ip_response.text

#Create self node representation
self_node = node.Node(constants.CLOUD_PROVIDERS(cloud_provider).name, cloud_region, current_public_ip, vm_instance)

#Connect with server
server_socket_connection = socket.socket()
server_socket_connection.connect((constants.SERVER_LOCATION_EC2_EAST, constants.RESERVED_PORT))
print("Sending node information to server at: ", constants.SERVER_LOCATION_EC2_EAST)
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
    recv_data = connection.recv(constants.BUFFER_SIZE)
    while recv_data:
        file.write(recv_data)
        break
        recv_data = connection.recv(constants.BUFFER_SIZE)
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
node_info_dict = helpers.read_node_locations()

#identify which node is self
for key, n in node_info_dict.items():
    if n.last_reachable_ipv4 == current_public_ip:
        n.is_self = True
        print("Found myself")

#Start pinging
#for key, n in node_info_dict.items():
#   if not n.is_self:
#       response = ping(n.last_reachable_ipv4, verbose=True)
#
#print('Done pinging')


#start threads = num_nodes
num_nodes = len(node_info_dict) - 1 #account for self node
print("Num nodes: ", num_nodes)
#create list of output files
thread_output_location_list = []
for i in range(num_nodes):
    thread_output_location_list.append(constants.OUTPUT_LOCATION+"/thread_"+str(i)+"_ping_measure")
for i in thread_output_location_list:
    print(i)
def write_ping_to_file(ip_path, file, nodeToPing):
    #capture source
    #       destination
    #       send_time
    #       rtt_avg
    #       recieve time (send + rtt)

    #Create line to write to file
    send_time = time()
    response = ping(ip_path, count=4)
    output = f"{current_public_ip},{ip_path},{send_time},{response.rtt_avg},{send_time+response.rtt_avg}\n"
    file.write(output)


def thread_ping_manager(output_path, ip_to_ping, times_to_ping, node_to_ping):
    output_file = open(output_path+"_"+node_to_ping.unique_name, "w")
    for i in range(times_to_ping):
        write_ping_to_file(ip_to_ping, output_file, nodeToPing=node_to_ping)
        sleep(1)
    output_file.close()
threads =[]
amount_to_ping = 15
i = 0
for k,n in node_info_dict.items():
    if not n.is_self:
        thread = threading.Thread(target=thread_ping_manager, args=(thread_output_location_list[i], n.last_reachable_ipv4, amount_to_ping, n))
        threads.append(thread)
        thread.start()
        i = i + 1

for thread in threads:
    thread.join()

print("Done pinging")

def write_wget_to_file(ip_path, file):

    #Create line to write to file
    filename = current_public_ip+".txt"
    start_time = time()
    response = wget.download("http://"+ip_path+":"+str(constants.WGET_PORT)+constants.WGET_URI, out=filename)
    end_time = time()
    os.remove(filename)
    output = f"{current_public_ip},{ip_path},{end_time - start_time},{constants.FILE_SIZE / (end_time - start_time)}\n"
    file.write(output)


def thread_wget_manager(output_path, ip_to_wget, times_to_wget, node_to_wget):
    output_file = open(output_path+"_"+node_to_wget.unique_name+"_wget", "w")
    for i in range(times_to_wget):
        write_wget_to_file(ip_to_wget, output_file)
        sleep(1)
    output_file.close()

wget_threads =[]
amount_to_wget = 5

i = 0
for k,n in node_info_dict.items():
    if not n.is_self:
        thread = threading.Thread(target=thread_wget_manager, args=(thread_output_location_list[i], n.last_reachable_ipv4, amount_to_wget, n))
        wget_threads.append(thread)
        thread.start()
        i = i + 1

for thread in wget_threads:
    thread.join()


print("Done wget")