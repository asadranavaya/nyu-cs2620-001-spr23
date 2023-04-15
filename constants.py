from enum import Enum
#Global constants to use

NODE_LOCATION = "inputs/node_locations.csv"
OUTPUT_LOCATION = "outputs"
GET_PUBLIC_IP_URL = "http://ipconfig.me"
START_SENDING = "start_sending"
INITIAL_RESPONSE_ACK_GOOD = "good"
INITIAL_RESPONSE_ACK_BAD = "bad"
SERVER_LOCATION_EC2_EAST = "44.215.3.14"
RESERVED_PORT = 7879
BUFFER_SIZE = 4096 #network file location buffersize
WGET_PORT = 8080
WGET_URI = "/test/test.txt"
FILE_SIZE = 1100009

class CLOUD_PROVIDERS(Enum):
    AWS = 1
    GCP = 2
    AZURE = 3

class AWS_REGIONS(Enum):
    US_EAST_1_VIRGINIA = 1
    US_EAST_2_OHIO = 2
    US_WEST_1_CALIFORNIA = 3
    US_WEST_2_OREGON = 4
    EU_CENTRAL_1_FRANKFURT = 5
    SA_EAST_1_SAO_PAULO = 6
    AP_SOUTHEAST_1_SINGAPORE = 7
    EU_NORTH_1_STOCKHOLM = 8

class GCP_REGIONS(Enum):
    US_SOUTH_1 = 1
    ASIA_EAST_1 = 2
    AUSTRALIA_SOUTHEAST_1 = 3
    EUROPE_NORTH_1 = 4
    US_CENTRAL_1 = 5

class AZURE_REGIONS(Enum):
    BRAZIL_SOUTH = 1
    FRANCE_CENTRAL = 2
    QATAR_CENTRAL = 3
    SOUTH_AFRICA_NORTH = 4
    JAPAN_EAST = 5
    US_EAST = 6

class AWS_INSTNACE_TYPES(Enum):
    T2_MICRO = 1
    T3_MICRO = 2
class GCP_INSTANCE_TYPES(Enum):
    E2 = 1
class AZURE_INSTANCE_TYPES(Enum):
    B1 = 1

#Errors
NODE_LOCATION_NOT_FOUND = "Location of Node information could not be found in top directory of scripts, please add it and continue."