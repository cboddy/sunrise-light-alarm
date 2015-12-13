from flask import Flask, request, session, redirect, url_for, escape, Session, make_response, jsonify, send_from_directory
from flask.ext.mail import Mail, Message
from itsdangerous import URLSafeSerializer, BadSignature

import os, sys, os.path
import functools
import urllib, urllib2
import time
from dateutil import parser
import traceback
import config
from alarm import *
import logging

WEEKDAYS = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}

#logging.basicConfig(format='%(asctime)s %(message)s', filename= "alarm.log", level=logging.DEBUG)

app = Flask(__name__)

def main():
    app.alarm = None
    if app.alarm is not None: app.alarm.start()

    app.debug = config.debug 
    app.secret_key = config.secretKey 
    app.statePath = config.statePath
    if os.path.exists(app.statePath): 
        state = AlarmState.fromFile(app.statePath)
        app.alarm = Alarm(state) 
        
    print("Starting with alarm", app.alarm)
    app.run(port=config.port, threaded=config.threaded)

def with_login(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        if not "username" in session:
            return json.dumps({"status": "error", "message": "Please log in."})
        request.username = session["username"]
        return f(*args, **kwds)
    return wrapper

@app.route("/<path:path>")
def static_content(path):
    return send_from_directory('public/', path)

@app.route("/")
def redirct_to_main():
    return send_from_directory('public/', "index.html")

@app.route("/set")
def set():
    args = request.args
    print("set request-args", args)
    date_time = parser.parse(args["time"])
    weekdays =  [WEEKDAYS[x] for x in args if x in WEEKDAYS]
    updatedState = AlarmState(date_time, weekdays)

    #finish current alarm
    if app.alarm is not None: 
        print("Finishing current alarm", app.alarm)
        app.alarm.close()

    #serialize updated state
    print("Updating state-file ", app.statePath)
    updatedState.toFile(app.statePath)

    #set and start updated alarm thread
    app.alarm = Alarm(updatedState)
    print("Starting updated alarm", app.alarm)
    app.alarm.start()
    
    return jsonify({"status": "OK"}) 

if __name__ == "__main__":
    main()
