import paramiko
import logging

error_log = logging.getLogger("error_logger")
server_log = logging.getLogger("request_log")

class SSHObject():
    def __init__(self) -> None:
        self.ssh_clients = {}
        pass

    def connect_ssh(self,host,user,password,port=22)->paramiko.SSHClient:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, port, user, password)
            self.ssh_clients[host] = ssh_client
            return (ssh_client,1)
        except Exception as er:
            error_log.error(f"ssh connection error --> {host}  {user}")
            return (str(er),0)

    def execute_cli(self,host,command):
        stdin, stdout, stderr = self.ssh_clients[host].exec_command(command)
        
        if stdout is not None:
            stdout = (stdout.read().decode())

        if stderr is not None:
            stderr = stderr.read().decode()
        stdin.close()

        return (stdout,stderr)

# obj = SSHObject()
# obj.connect_ssh("localhost","gowthaman","12345")
# obj.execute_cli("localhost","ifconfig")