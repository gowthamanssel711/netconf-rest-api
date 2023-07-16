"""
NetConfController File consists netconf operation functions.

Date: July 15, 2023
"""
from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
from netconf_constants.NetConfConstants import NetConfConstants
from controller.SSHObject import SSHObject
import logging
import inspect

error_log = logging.getLogger("error_logger")
server_log = logging.getLogger("request_log")

class NetConfController:

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