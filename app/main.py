"""
Application server.

Date: July 15, 2023
"""
from controller.NetConfController import NetConfController
from flask import Flask,request,jsonify
from logger.Log import *



app = Flask(__name__)
netconf_controller = NetConfController()
init_loggers('Logs/server.log', 'Logs/error.log')
server_Log = logging.getLogger("request_log")


@app.route("/connect_client",methods=["POST"])
def connect_client():
    server_Log.info(f"request to connect client {request.get_json()}")
    code  = 400
    client = False
    try:
        client_details = request.get_json()
        client = netconf_controller.netconf_client(**client_details)
        code = 200
    except Exception as e:
        code = 400

    return jsonify({
        'connected':client[0],
        'error':client[1]
    }),code


@app.route("/get_interface",methods=["POST"])
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

app.run(host='0.0.0.0',debug=True)