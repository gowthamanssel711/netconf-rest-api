"""
NetConfConstants File consists of xml structure for basic operations.

Date: July 15, 2023
"""
from netconf_constants.constants import *

class NetConfConstants:
    
    def __init__(self) -> None:
        pass

    def filter_tag(self,interface_name:str)-> str:
        return filter_tag.format(interface_name=interface_name)

    def add_configuration(self,name,description,ip,subnetmask,host='')->str:
        return add_configuration.format(
            interface_name = name,
            interface_description = f"{description} {host}",
            ip_address = ip,
            subnet_mask = subnetmask
        )
    
    def delete_configuration(self,operation:str,interface_name:str)->str:
        return delete_configuration.format(
            operation = operation,
            interface_name = interface_name
        )
