"""
Copyright (C) 2020 Kratrim Labs - All Rights Reserved.

To use this, wrap `4_here_maps.py` into a function first.
"""
import flask
from flask import request, jsonify, render_template

import pandas as pd
from here_nav_api import find_route
import requests

# %%
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# http://127.0.0.1:5000/api/v1/routes?src=12.973132,77.601479&tgt=12.977664,77.638843
# results = find_route("12.973132,77.601479","12.977664,77.638843")


@app.route("/")
def my_form():
    return render_template("my-form.html")


@app.route("/", methods=["POST"])
def my_form_post():
    start = request.form["start"]
    end = request.form["end"]
    results = find_route(str(start), str(end))
    return results.__geo_interface__


@app.route("/api/v1/routes", methods=["GET"])
def api_id():
    if "src" in request.args:
        src = request.args["src"]
    else:
        return "Error: No src field provided."

    if "tgt" in request.args:
        tgt = request.args["tgt"]
    else:
        return "Error: No tgt field provided."

    # Create an dummy list for our results
    results = find_route(src, tgt)

    # here_api = "5CXu_n0rUCdURLzwlrWd42CFNXvbMP0ceiPFyjTWIJQ"
    # address= "https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey="+here_api+"&waypoint0=geo!"+src+"&waypoint1=geo!"+tgt+"&departure=now&mode=fastest;publicTransport&combineChange=true"
    # response = requests.get(address)

    return results.__geo_interface__  # jsonify(results)


app.run()
