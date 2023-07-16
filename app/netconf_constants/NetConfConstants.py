"""
NetConfConstants File consists of xml structure for basic operations.

Date: July 15, 2023
"""
from netconf_constants.constants import *

class NetConfConstants:
    """
    A class that provides constants and utility functions for NETCONF operations.

    Methods:
        - filter_tag: Generates a filter tag for filtering configuration based on an interface name.
        - add_configuration: Generates a add inteface tag  for adding an interface.
        - delete_configuration: Generates a delete tag snippet for deleting an interface.

    """
    
    def __init__(self) -> None:
        pass

    def filter_tag(self,interface_name:str,all=False)-> str:
        """
        Generates a filter tag for filtering configuration based on an interface name.

        Args:
            interface_name (str): The name of the interface.

        Returns:
            The generated filter tag as a string.

        """
        if all:
            return all_interface
        return filter_tag.format(interface_name=interface_name)

    def add_configuration(self,name,description,ip,subnetmask,host='')->str:
        """
        Generates a configuration snippet for adding an interface.

        Args:
            name (str): The name of the interface.
            description (str): The description of the interface.
            ip (str): The IP address of the interface.
            subnetmask (str): The subnet mask of the interface.
            host (str, optional): The host information. Defaults to an empty string.

        Returns:
            The generated configuration snippet as a string.

        """
        return add_configuration.format(
            interface_name = name,
            interface_description = f"{description} {host}",
            ip_address = ip,
            subnet_mask = subnetmask
        )
    
    def delete_configuration(self,operation:str,interface_name:str)->str:
        """
        Generates a configuration snippet for deleting an interface.

        Args:
            operation (str): The operation to be performed (e.g., 'delete').
            interface_name (str): The name of the interface to be deleted.

        Returns:
            The generated configuration snippet as a string.

        """
        return delete_configuration.format(
            operation = operation,
            interface_name = interface_name
        )
