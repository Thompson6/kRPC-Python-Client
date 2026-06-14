from flask import Flask, make_response, redirect, render_template, request, url_for, jsonify
import datetime
import json

from flask_wtf import FlaskForm
from wtforms import SubmitField

from waitress import serve

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
        "gforce": ship.g_force()
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
    
def add_return_cookie(input):
    response = make_response(input)
    response.set_cookie("return_cookie", "value")
    print("Set a return cookie")
    return response

if __name__ == "__main__":
    serve(app, listen=f'*:{web_port}')