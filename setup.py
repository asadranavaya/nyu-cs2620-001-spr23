import constants
import node
import os.path
import csv

#check validity
if(not os.path.exists(constants.NODE_LOCATION) or not os.path.isfile(constants.NODE_LOCATION)):
    raise FileNotFoundError(constants.NODE_LOCATION_NOT_FOUND)
#read in locations and update the data structures
node_list = [];

with open(constants.NODE_LOCATION, newline='') as csvfile:
    nodeReader = csv.reader(csvfile, delimiter=",")
    next(nodeReader, None) #skip the headers
    for row_as_node in nodeReader:
        node_list.append(node.Node(row_as_node[0], row_as_node[1], row_as_node[2], row_as_node[3]))

for i in node_list:
    print(i)
