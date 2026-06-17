from flask import Flask, make_response, redirect, render_template, request, url_for, jsonify
import datetime
import json

from flask_wtf import FlaskForm
from wtforms import SubmitField

from gevent.pywsgi import WSGIServer

from flask_socketio import SocketIO, emit

try:
    from interface import kRPC_Interface as ship
except:
    ship = None

with open("config.json", "r") as f:
    config = json.load(f)

secret_key = config["secret_key"]
web_port = config["web_port"]

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key

socketio = SocketIO(app)

# User facing routes end with slashes
@app.route("/dashboard/", methods=["GET", "POST"])
def home():
    
    cookie = request.cookies.get("return_cookie")
    if not cookie:
        print("This is their first time") # User isn't coming from a function route
        response = make_response(render_template("dashboard.html", animate = True))
    else: 
        # User reloaded the page from a route so we don't need to bother playing the animation
        response = make_response(render_template("dashboard.html", animate = False))
        response.delete_cookie("return_cookie")
        
    return response

# Root route redirects to dashboard for convenience
@app.route("/", methods = ["GET"])
def root():
    return redirect(url_for("home"))

# Utilitarian routes do not end with slashes
@app.route("/telemetry")
def telemetry():
    
    data = {
        "altitude": ship.altitude(),
        "heading": ship.heading(),
        "pitch": ship.pitch(),
        "gforce": ship.g_force(),

        "s1e1": ship.s1e1_stream(),
        "s1e2": ship.s1e2_stream(),
        "s1e3": ship.s1e3_stream(),
        "s1e4": ship.s1e4_stream(),
        "s1e5": ship.s1e5_stream(),
        "s1e6": ship.s1e6_stream(),
        "s1e7": ship.s1e7_stream(),
    }

    return jsonify(data)

@app.route("/abort", methods=["GET", "POST"])
def abort_page():
    if ship:
        ship.abort_mission()
    response = add_return_cookie(redirect(url_for("home")))
    return response

@app.route("/gear", methods=["GET", "POST"])
def gear_page():
    if ship:
        ship.toggle_gear()
    response = add_return_cookie((redirect(url_for("home"))))
    return response

@app.route("/engine/<stage>/<engine_number>", methods=["GET", "POST"])
def engine_page(stage, engine_number):
    if ship:
        ship.toggle_engine(stage, engine_number)
    response = add_return_cookie((redirect(url_for("home"))))
    return response
    
def add_return_cookie(input):
    response = make_response(input)
    response.set_cookie("return_cookie", "value")
    print("Set a return cookie")
    return response

# @socketio.on('set_engines')
# def broadcast_all_engines():
#     print("HEY WE GOT SOME ENGINES OVER HEREEEE!!!")
#     engines = []
#     for engine in range(7): # Stage hard coded to 1 bc we don't have stage 2 yet
#         status = ship.get_engine_status(1, engine+1)
#         engines.append(status)
#     emit('all_engines', engines, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)