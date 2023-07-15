"""
Application server.

Date: July 15, 2023
"""
from controller.NetConfController import NetConfController
from response.response import *
from flask import Flask,request,jsonify

app = Flask(__name__)
netconf_controller = NetConfController()


@app.route("/connect_client",methods=["POST"])
def connect_client():
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


app.run(host='0.0.0.0',debug=True)