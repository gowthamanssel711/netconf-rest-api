import paramiko
import logging

error_log = logging.getLogger("error_logger")
server_log = logging.getLogger("request_log")

class SSHObject():
    def __init__(self) -> None:
        self.ssh_clients = {}
        pass

    def connect_ssh(self,host,user,password,port=22)->paramiko.SSHClient:
        """
        Establishes an SSH connection with the specified host.

        Args:
            host (str): The hostname or IP address of the device.
            user (str): The username for SSH authentication.
            password (str): The password for SSH authentication.
            port (int, optional): The port number for the SSH connection. Defaults to 22.

        Returns:
            A tuple containing the SSH client object and a status code.

            If the SSH connection is established successfully:
                - The SSH client object
                - 1 for the status code

        Raises:
            If there's an error connecting to the SSH host:
                - An exception containing the error message.

        Note:
            This method uses the paramiko library to establish the SSH connection.
            The SSH client object is stored in the 'ssh_clients' attribute for future reference.

        """
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
        """
        Executes a command on the CLI of the specified host.

        Args:
            host (str): The hostname or IP address of the device.
            command (str): The command to be executed on the CLI.

        Returns:
            A tuple containing the stdout and stderr of the executed command.

            If the command is executed successfully:
                - The stdout of the executed command
                - The stderr of the executed command

        Note:
            This method assumes that the SSH connection has been established and the SSH client object is stored in the 'ssh_clients' attribute.

        """
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