#defines a cloud node vm
class Node:
    def __init__(self, cloud_provider, cloud_region, last_reachable_ipv4, instance_type):
        self.cloud_provider = cloud_provider
        self.cloud_region = cloud_region
        self.last_reachable_ipv4 = last_reachable_ipv4
        self.instance_type = instance_type
        self.unique_name = self.cloud_provider +"-"+ self.cloud_region
        self.has_recieved_initial_ack = False
        self.is_self = False

    def __str__(self):
        return f"{self.cloud_provider},{self.cloud_region},{self.last_reachable_ipv4},{self.instance_type}"