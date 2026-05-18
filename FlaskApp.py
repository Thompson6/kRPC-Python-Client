from flask import Flask, make_response, redirect, render_template, request, url_for
import datetime
import json

from flask_wtf import FlaskForm
from wtforms import SubmitField

from interface import kRPC_Interface as ship

app = Flask(__name__)
app.config["SECRET_KEY"] = "jimmy"


@app.route("/dashboard/", methods=["GET", "POST"])
def home():
    return render_template("dashboard.html")


@app.route("/abort/", methods=["GET", "POST"])
def abort_page():
    ship.abort_mission()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()