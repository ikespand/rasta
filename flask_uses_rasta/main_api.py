"""
ikespand@GitHub

Implemention of a REST API| for our function which itself fetch data from the
OSM and do some calculation based on Flask.
"""
import sys

sys.path.append("/Users/ikespand/Desktop/rasta/")
from settings import MAPBOX_API_KEY  # THIS HOLDS API KEYS
from rasta.navigate_with_otp import GetOtpRoute
import flask
from flask import request, render_template

# BELOW IS A SAMPLE API CALL
# http://127.0.0.1:5000/api/v1/navigation?src=28.69782,77.19269&tgt=28.60743,77.22702
# %%
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def visualize_with_kepler(start_coord, end_coord):
    """A wrapper for the class for OTP to unify web and api interface."""
    my_otp_nav = GetOtpRoute(
        start_coord=start_coord,
        end_coord=end_coord,
        MAPBOX_API_KEY=MAPBOX_API_KEY,
        output_map_path="templates/temporary_map_",
    )

    gdf, html_path = my_otp_nav.extract_itinerary()
    return gdf, html_path


@app.route("/")
def my_form():
    """Home page of our api"""
    return render_template("src_tgt_radius.html")


@app.route("/", methods=["POST"])
def my_form_post():
    """Take the data from our form and provide the results."""
    src = request.form["src"]
    tgt = request.form["tgt"]
    if not len(src) > 0:
        return "Error: No or bad source field!"
    elif not len(tgt) > 0:
        return "Error: No or bad source field!"
    else:
        gdf, _ = visualize_with_kepler(start_coord=src, end_coord=tgt)

        # return results#.__geo_interface__
        return render_template("temporary_map_vis.html")


@app.route("/api/v1/navigation", methods=["GET"])
def api_id():
    """Returns the data with web request."""
    if "src" in request.args and "tgt" in request.args:
        src = request.args["src"]
        tgt = request.args["tgt"]
    else:
        return "Error: No src/tgt field provided."

    # results = navigate_me(start_coord=src, end_coord=tgt)
    results, _ = visualize_with_kepler(start_coord=src, end_coord=tgt)

    # There are multiple iternaries, but for now returning the first one
    return results[0].__geo_interface__


# %%
if __name__ == "__main__":
    app.run()
