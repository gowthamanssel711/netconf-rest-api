"""
Application server.

Date: July 15, 2023
"""
from controller.NetConfController import NetConfController
from flask import Flask,request,jsonify
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
    server_Log.info(f"request to connect client  ---> {request.get_json()}")
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
    server_Log.info(f"request to get interface {request.get_json()}")
    code = 400
    try:
        client_details = request.get_json()
        interface = netconf_controller.filter_config(**client_details)
        code = 200
    except Exception as e:
        code = 400

    return jsonify({
        "interface":interface[0],
        "error":interface[1]
    }),code


@app.route("/execute_cli",methods=["POST"])
@validate_params(execute_cli)
def execute_cli():
    server_Log.info(f"execure commands in cli {request.get_json()}")
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

app.run(host='0.0.0.0',debug=True)