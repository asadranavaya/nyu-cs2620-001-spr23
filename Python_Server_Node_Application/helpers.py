import constants
import os.path
import node
import csv

#Reads location of nodes from csv file and returns a dictionary of mapped nodes
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

#Prints enum and returns user response as integer
def print_enum_get_response(enumToPrint):
    print("Please select a value:")
    for i in range(1, len(enumToPrint)+1):
        print(f"{i}. {enumToPrint(i).name}")
    return int(input(""))

def print_enum_get_response_as_string(enumToPrint):
    print("Please select a value:")
    for i in range(1, len(enumToPrint)+1):
        print(f"{i}. {enumToPrint(i).name}")
    return enumToPrint(int(input(""))).name

#Returns enum from provided integer
#AMAZON EC2 does not come with python3.10 :(
def match_to_region(enumToMatch):
    if enumToMatch == 1:
        return constants.AWS_REGIONS
    elif enumToMatch == 2:
        return constants.GCP_REGIONS
    elif enumToMatch == 3:
        return constants.AZURE_REGIONS
    #match enumToMatch:
    #    case 1:
    #        return constants.AWS_REGIONS
    #    case 2:
    #        return constants.GCP_REGIONS
    #    case 3:
    #        return constants.AZURE_REGIONS

def match_to_instance(enumToMatch):
    if enumToMatch == 1:
        return constants.AWS_INSTNACE_TYPES
    elif enumToMatch == 2:
        return constants.GCP_INSTANCE_TYPES
    elif enumToMatch == 3:
        return constants.AZURE_INSTANCE_TYPES
        
#response = print_enum_get_response(constants.CLOUD_PROVIDERS)
#print(constants.CLOUD_PROVIDERS(response).name)