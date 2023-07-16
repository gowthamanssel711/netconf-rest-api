"""
Application server to execute Netconf interface CRUD Operations and 
cli execute.

Date: July 15, 2023
"""
import os
import sys
from controller.NetConfController import NetConfController
from flask import Flask,request,jsonify,make_response
from logger.Log import *
from utils.param_validator import validate_params
from utils.request_params import *


app = Flask(__name__)
netconf_controller = NetConfController()
init_loggers('Logs/server.log', 'Logs/error.log')
server_Log = logging.getLogger("request_log")


@app.route("/connect_client",methods=["POST"])
@validate_params(connect_client)
def connect_client():
    """
    Connects a client using Netconf.

    Args:
        host (str): The hostname or IP address of the client.
        password (str): The password to authenticate the client.
        user (str) : The user name .
        port : 22 for ssh and 830 for Netconf (default 830)

    Returns:
        A JSON response with the connection status and error message.

        If the connection is successful:
            - 'connected': 'True'
            - 'error': None

        If the connection fails:
            - 'connected': 'False'
            - 'error': Error message describing the failure

    HTTP Status Codes:
        - 200: Success (if 'error' is None)
        - 500: Internal Server Error (if 'error' is not None)
    """
    server_Log.info(f"request to connect client  ---> {request.get_json()} | ip =  {request.remote_addr}")
    client = False
    try:
        client_details = request.get_json()
        client = netconf_controller.netconf_client(**client_details)
    except Exception as e:
        server_Log.error("connect client error = {e}")

    return jsonify({
        'connected':str(client[0]),
        'error':client[1]
    }),500 if client[1] else 200


@app.route("/get_interface",methods=["POST"])
@validate_params(get_interface)
def get_interface():
    """
    Retrieves interface information using Netconf.

    Args:
        host (str): The hostname or IP address of the device.
        interface (str) : To filter the particular interface. 
        Without interface payload : return all interfaces.

    Returns:
        A JSON response with the interface details and error message.

        If the interface information is successfully retrieved:
            - 'interface': Interface details
            - 'error': None

        If there's an error retrieving the interface information:
            - 'interface': None
            - 'error': Error message describing the failure

    HTTP Status Codes:
        - 200: Success (if 'error' is None)
        - 400: Bad Request (if 'error' is not None)
    """
    server_Log.info(f"request to get interface {request.get_json()} | ip =  {request.remote_addr}")
    code = 400
    try:
        client_details = request.get_json()
        interface = netconf_controller.filter_config(**client_details)
        if interface[0] != False:
                response = make_response(interface[0])
                response.headers['Content-Type'] = 'application/xml'
        code = 200
    except Exception as e:
        code = 400
        response = jsonify({
        "interface":interface[0],
        "error":interface[1]
    })

    return response,code


@app.route("/add_interface",methods=["POST"])
@validate_params(add_interface)
def add_interface():
    """
    Adds a new interface using Netconf.

    Args:
        host (str): The hostname or IP address of the device.
        name (str): The name of the interface to be added.
        description (str): The description of the interface.
        ip (str): The IP address of the interface.
        subnetmask (str): The subnet mask of the interface.

    Returns:
        A JSON response with the output and error message.

        If the interface is successfully added:
            - 'output': Output message indicating the success
            - 'error': None

        If there's an error adding the interface:
            - 'output': None
            - 'error': Error message describing the failure

    HTTP Status Code:
        - 200: Success (if 'error' is None)

    Note:
        The 'output' field can contain any response or success message specific to the Netconf controller.

    """
    server_Log.info(f"request to add  interface {request.get_json()} | ip =  {request.remote_addr}")
    output = ''
    error = ''
    try:
        interface_details = request.get_json()
        output,error = netconf_controller.add_interface(**interface_details)
    except Exception as e:
        error = e
    return jsonify({
        "output":output,
        "error":error
    })



@app.route("/delete_interface",methods=["DELETE"])
@validate_params(delete_interface)
def delete_interface():
    """
    Deletes an interface using Netconf.

    Args:
        host (str): The hostname or IP address of the device.
        interface_name (str): The name of the interface to be deleted.

    Returns:
        A JSON response with the output and error message.

        If the interface is successfully deleted:
            - 'output': Output message indicating the success
            - 'error': None

        If there's an error deleting the interface:
            - 'output': None
            - 'error': Error message describing the failure

    HTTP Status Code:
        - 200: Success (if 'error' is None)

    Note:
        The 'output' field can contain any response or success message specific to the Netconf controller.

    """
    server_Log.info(f"request to delete interface {request.get_json()} |  ip =  {request.remote_addr}")
    output = ''
    error = ''
    try:
        interface_details = request.get_json()
        output,error = netconf_controller.delete_interface(**interface_details)
    except Exception as err:
        error = err
    return jsonify({
        "output": output,
        "error": error
    })

@app.route("/execute_cli",methods=["POST"])
@validate_params(execute_cli)
def execute_cli():
    """
    Executes CLI commands on a device using SSH.

    Args:
        host (str): The hostname or IP address of the device.
        command (str): The command to be executed on the device's CLI.

    Returns:
        A JSON response with the command output and error message.

        If the command execution is successful:
            - 'output': Output of the executed command
            - 'error': None

        If there's an error executing the command:
            - 'output': None
            - 'error': Error message describing the failure

    HTTP Status Code:
        - 200: Success (if 'error' is None)

    """
    server_Log.info(f"execure commands in cli {request.get_json()} | ip =  {request.remote_addr}")
    stdout = ''
    stderr = ''
    try:
        commands = request.get_json()
        stdout,stderr = netconf_controller.execute_cli(**commands)
    except Exception as e:
        stderr = str(e)
    return jsonify({
        'output':stdout,
        'error':stderr
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)