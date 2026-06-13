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
    return render_template("dashboard.html")

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
    ship.abort_mission()
    return redirect(url_for("home"))

@app.route("/gear", methods=["GET", "POST"])
def gear_page():
    ship.toggle_gear()
    return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run()