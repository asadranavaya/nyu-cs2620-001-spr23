#Global constants to use

NODE_LOCATION = "inputs/node_locations.csv"
GET_PUBLIC_IP_URL = "http://169.254.169.254/latest/meta-data/public-ipv4"
START_SENDING = "start_sending"
INITIAL_RESPONSE_ACK_GOOD = "good"
INITIAL_RESPONSE_ACK_BAD = "bad"
AWS_CLOUD = "AWS"
AWS_INSTANCE_T2 = "t2.micro"
SERVER_LOCATION_EC2_EAST = "44.215.3.14"
RESERVED_PORT = 7879
BUFFER_SIZE = 4096 #network file location buffersize
#Errors
NODE_LOCATION_NOT_FOUND = "Location of Node information could not be found in top directory of scripts, please add it and continue."