from flask import Flask, request, session, redirect, url_for, escape, Session, make_response, jsonify, send_from_directory
from flask.ext.mail import Mail, Message
from itsdangerous import URLSafeSerializer, BadSignature

import os, sys
import functools
import urllib, urllib2
import time
import dateutil.parser
import traceback

import config

app = Flask(__name__)
 
def main():
    app.debug = config.debug 
    app.secret_key = config.secretKey 
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
    return jsonify({"status": "OK"}) 
if __name__ == "__main__":
    main()

