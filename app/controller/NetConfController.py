"""
NetConfController File consists netconf operation functions.

Date: July 15, 2023
"""
from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
from netconf_constants.NetConfConstants import NetConfConstants
from controller.SSHObject import SSHObject
import logging

error_log = logging.getLogger("error_logger")
server_log = logging.getLogger("request_log")

class NetConfController:
    """
    A class that provides control and management functionalities for NETCONF operations.

    Methods:
        - netconf_client: Establishes a NETCONF client connection with the specified device.
        - ssh_connect: Establishes an SSH connection with the specified host.
        - execute_cli: Executes a command on the CLI of the specified host.
        - add_interface: Adds a new interface configuration using NETCONF.
        - delete_interface: Deletes an interface configuration using NETCONF.
        - filter_config: Retrieves the filtered configuration for a specific interface using NETCONF.

    """

    def __init__(self) -> None:
        self.clients = {}
        self.ssh_clients = {}
        self.client_info = {}
        self.nc_const = NetConfConstants()
        self.ssh_con = SSHObject()
        pass

    def _func_params(self,params)->dict:
        _param = params.copy()
        _param.pop('self')
        return _param
    


    def netconf_client(self, host: str, user: str, password:str, port=830) -> Manager:
        """
        Establishes a NETCONF client connection with the specified device.

        Args:
            host (str): The hostname or IP address of the device.
            user (str): The username for authentication.
            password (str): The password for authentication.
            port (int, optional): The port number for the NETCONF connection. Defaults to 830.

        Returns:
            If the client connection is established successfully:
                - An instance of the NETCONF Manager class.

        Raises:
            If there's an error connecting to the client:
                - An exception containing the error message.

        Note:
            This method internally uses SSH or NETCONF connections based on the provided port number.

        """
        param = self._func_params(locals())
        try:
            if port == 22:
                param['port'] = 22
                ssh = self.ssh_connect(**param)
                return ssh
            session = connect_ssh(host=host, port=port,
                                username=user, password=password)
            nc_mgr = Manager(session, timeout=120)
            self.clients[host] = nc_mgr
            self.client_info[host]=param
            server_log.info(f"client connected ---> {param} ")
            return (True,0)
        except Exception as error:
            error_log.error(f" {param} --> connect client error  = {error}")
            return (False,str(error))

    def ssh_connect(self,**args):
        """
        Establishes an SSH connection with the specified host.

        Args:
            host (str): The hostname or IP address of the device.
            user (str): The username for SSH authentication.
            password (str): The password for SSH authentication.
            port (int, optional): The port number for the SSH connection. Defaults to 22.

        Returns:
            If the SSH connection is established successfully:
                - An SSHClient object.

        Raises:
            If there's an error connecting to the SSH host:
                - An exception containing the error message.

        Note:
            This method assumes that an SSHClient object is used for establishing the SSH connection.

        """
        try:
           ssh = self.ssh_con.connect_ssh(**args)
           if ssh[1]:
               self.ssh_clients[args['host']] = ssh[0]
               return (True,0)
           return (False,1)
        except Exception as e:
            error_log.error(f"SSH connection failed == {e}")
            return (False,str(e))


    def execute_cli(self,**args):
        """
        Executes a command on the CLI of the specified host.

        Args:
            host (str): The hostname or IP address of the device.
            command (str): The command to be executed on the CLI.

        Returns:
            A tuple containing the output and error message of the executed command.

        Raises:
            If there's an error executing the command:
                - An exception containing the error message.

        Note:
            This method internally establishes an SSH connection if necessary and uses an SSHClient object for executing the command.
    ``  """
        op = ('','')
        try:
            if (args['host']) not in self.ssh_clients:
               ssh_credential = args.copy()
               ssh_credential.pop('command')
               ssh =  self.ssh_connect(**ssh_credential)
               if ssh[0]:
                  op =  self.ssh_con.execute_cli(args['host'],args['command'])
            else:
                op =  self.ssh_con.execute_cli(args['host'],args['command'])
        except Exception as e:
            error_log.error(f"execute cli failed  == {e}")
            op = ('',str(e))
        return op

    def add_interface(self,**args):
        """
        Adds a new interface configuration using NETCONF.

        Args:
            host (str): The hostname or IP address of the device.
            interface_name (str): The name of the interface to be added.

        Returns:
            A tuple containing the NETCONF response and error message.

            If the interface is successfully added:
                - '': Netconf response 
                - '' for the error message

            If there's an error adding the interface:
                - NETCONF response message
                - Error message describing the failure

        Note:
            This method assumes that the NETCONF client is already connected and stored in the 'clients' attribute.

        """
        nc_response = ''
        try:
            if (args['host'] not in self.clients):
                return ('','client not connected')
            add_tag = self.nc_const.add_configuration(**args)
            nc_response = self.clients[args['host']].edit_config(add_tag,target='running')
        except Exception as e:
            return (nc_response,str(e))
        return (nc_response,'')


    def delete_interface(self,**args):
        """
        Deletes an interface configuration using NETCONF.

        Args:
            host (str): The hostname or IP address of the device.
            interface_name (str): The name of the interface to be deleted.

        Returns:
            A tuple containing the NETCONF response and error message.

            If the interface is successfully deleted:
                - '': Netconf Response
                - '' for the error message

            If there's an error deleting the interface:
                - NETCONF response message
                - Error message describing the failure

        Note:
            This method assumes that the NETCONF client is already connected and stored in the 'clients' attribute.

        """
        nc_response = ''
        try:
            if (args['host'] not in self.clients):
                return ('','client not connected')
            delete_tag = self.nc_const.delete_configuration(interface_name=args['interface_name'],operation='delete')
            print(delete_tag)
            nc_response = self.clients[args['host']].edit_config(delete_tag,target='running')
        except Exception as e:
            return (nc_response,str(e))
        return (nc_response,'')

    def filter_config(self, host="localhost", user=None, password=None, interface=None):
        """
        Retrieves the filtered configuration for a specific interface using NETCONF.

        Args:
            host (str): The hostname or IP address of the device. Defaults to "localhost".
            user (str): The username for authentication. Defaults to None.
            password (str): The password for authentication. Defaults to None.
            interface (str): The interface name to filter the configuration. Defaults to None.

        Returns:
            A tuple containing the filtered configuration and error message.

            If the filtered configuration is successfully retrieved:
                - The filtered configuration as a string
                - 0 for the error message

            If there's an error retrieving the filtered configuration:
                - False for the filtered configuration
                - Error message describing the failure
        """
        try:
            tag = self.nc_const.filter_tag(interface)
            if host not in self.clients:
                self.netconf_client(host, user, password)
            result = self.clients[host].get_config('running', tag).data_xml
            return (str(result),0)
        except Exception as error:
            error_log.error(f" {self._func_params(locals())} --> ilter enterface error = {error}")
            return (False,str(error))


# obj = NetConfController()
# res = obj.netconf_client(host="localhost",user="gowthaman",password="12345")
# res = obj.filter_config(host="localhost")