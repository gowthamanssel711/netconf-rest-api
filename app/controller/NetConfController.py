"""
NetConfController File consists netconf operation functions.

Date: July 15, 2023
"""
from netconf_client.connect import connect_ssh
from netconf_client.ncclient import Manager
from netconf_constants.NetConfConstants import NetConfConstants
import logging

error_log = logging.getLogger("error_logger")

class NetConfController:

    def __init__(self) -> None:
        self.clients = {}
        self.nc_const = NetConfConstants()
        pass

    def netconf_client(self, host: str, user: str, password:str, port=830) -> Manager:
        try:
            session = connect_ssh(host=host, port=port,
                                username=user, password=password)
            nc_mgr = Manager(session, timeout=120)
            self.clients[host] = nc_mgr
            return (True,0)
        except Exception as e:
            error_log.error(f"connect client error  = {e}")
            return (False,str(e))
        

    def filter_config(self, host="localhost", user=None, password=None, interface=None):
        try:
            tag = self.nc_const.filter_tag(interface)
            if host not in self.clients:
                self.netconf_client(host, user, password)
            result = self.clients[host].get_config('running', tag).data_xml
            return (str(result),0)
        except Exception as e:
            error_log.error(f"filter enterface error = {e}")
            return (False,str(e))


# obj = NetConfController()
# res = obj.netconf_client(host="localhost",user="gowthaman",password="12345")
# res = obj.filter_config(host="localhost")