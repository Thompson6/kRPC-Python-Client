from flask import Flask, make_response, redirect, render_template, request, url_for, jsonify
import datetime
import json

from flask_wtf import FlaskForm
from wtforms import SubmitField

from interface import kRPC_Interface as ship

app = Flask(__name__)
app.config["SECRET_KEY"] = "jimmy"

# User facing routes end with slashes
@app.route("/dashboard/", methods=["GET", "POST"])
def home():
    
    cookie = request.cookies.get("return_cookie")
    if not cookie:
        print("This is their first time")
    response = make_response(render_template("dashboard.html"))
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
        "altitude": ship.surface_altitude(),
        "heading": ship.heading(),
        "pitch": ship.pitch(),
        "gforce": ship.g_force()
    }

    return jsonify(data)

@app.route("/abort", methods=["GET", "POST"])
def abort_page():
    try:
        ship.abort_mission()
    except NameError:
        print("We didn't have a ship")
    response = add_return_cookie(redirect(url_for("home")))
    return response

@app.route("/gear", methods=["GET", "POST"])
def gear_page():
    try:
        ship.toggle_gear()
    except NameError:
        print("We didn't have a ship")
    response = add_return_cookie((redirect(url_for("home"))))
    return response
    
def add_return_cookie(input):
    response = make_response(input)
    response.set_cookie("return_cookie", "value")
    print("Set a return cookie")
    return response

if __name__ == "__main__":
    app.run()