"""
This script usage the HERE MAPS API to determine the fastest public transit
route.
This will act as rest api which will return geojson data for (upto) 3 available
options.

@author: ikespand
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import math
import requests
import numpy as np
from shapely.geometry import Point, LineString
from itertools import groupby
from process_geo_data import ProcessGeoData

# Install local version of keplergl_cli by:
# pip install git+https://github.com/ikespand/keplergl_cli

# %% Get data from HERE


class GetHereRoute:
    """Navigation with HERE maps. More info about the API:
    https://developer.here.com/documentation/routing-api/8.8.0/dev_guide/topics/use-cases/calculate-route.html
    """

    def __init__(self, start_coord, end_coord, HERE_API_KEY, departure=None):
        self.src = start_coord
        self.tgt = end_coord
        self.here_api_key = "?apiKey=" + HERE_API_KEY
        self.base_address = (
            "https://route.ls.hereapi.com/routing/7.2/calculateroute.json"
        )
        # Below options can be extended easily. For now, we don't need it.
        self.options = (
            "&departure=now&mode=fastest;publicTransport&combineChange=true"
        )
        self.request_address = (
            self.base_address
            + self.here_api_key
            + "&waypoint0=geo!"
            + self.src
            + "&waypoint1=geo!"
            + self.tgt
            + self.options
        )
        self.json_data = self.get_data_from_here()
        self.nav_data_df = self.json_to_df()

    def get_data_from_here(self):
        response = requests.get(self.request_address)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return "Server error!"
        else:
            return "No respose."

    def json_to_df(self):
        response_json = self.json_data
        maneuver_type = []
        coordinate_lat = []
        coordinate_lon = []
        instruction = []
        for k in response_json["response"]["route"][0]["leg"][0]["maneuver"]:
            # print(k["_type"])
            maneuver_type.append(k["_type"])
            coordinate_lat.append(k["position"]["latitude"])
            coordinate_lon.append(k["position"]["longitude"])
            instruction.append(k["instruction"])

        nav_data = pd.DataFrame()
        nav_data["type"] = maneuver_type
        nav_data["latitude"] = coordinate_lat
        nav_data["longitude"] = coordinate_lon
        nav_data["instruction"] = instruction
        nav_data["distance"] = ProcessGeoData.get_distance_from_df(nav_data)
        return nav_data

    def json_to_gdf(self):
        gdf_nav = []
        pt = []
        for k in range(0, len(self.nav_data_df)):
            pt.append(
                (
                    self.nav_data_df.loc[k].longitude,
                    self.nav_data_df.loc[k].latitude,
                )
            )

            if k != 0:
                __gdf = gpd.GeoDataFrame(
                    self.nav_data_df.loc[[k]],
                    crs="EPSG:4326",
                    geometry=[LineString([Point(pt[k - 1]), Point(pt[k])])],
                )
            else:
                __gdf = gpd.GeoDataFrame(
                    self.nav_data_df.loc[[k]], geometry=[Point(pt[k])]
                )

            gdf_nav.append(__gdf)
        gdf_nav = pd.concat(gdf_nav)
        return gdf_nav


# %% Main program to demonstrate the usage


if __name__ == "__main__":
    from keplergl_cli.keplergl_cli import Visualize

    start_coord = "12.874132,77.661479"  # Should come from the request
    end_coord = "12.877664,77.665843"  # Should come from the request

    HERE_API_KEY = "PASTE_YOUR_HERE_MAP_API"
    MAPBOX_API_KEY = "PASTE_YOUR_MAPBOX_API"

    my_here_route = GetHereRoute(start_coord, end_coord, HERE_API_KEY)
    json_data = my_here_route.json_data
    nav_data = my_here_route.nav_data_df
    # nav_data.to_csv("nav.csv", index=False)

    gdf = my_here_route.json_to_gdf()
    # gdf.to_file(start_coord+"_"+end_coord+".json", driver="GeoJSON")

    # Visualize with Kepler

    vis = Visualize(api_key=MAPBOX_API_KEY, output_map="Here-Route-Kepler")
    # Add the data to Visualize
    vis.add_data(data=gdf, names="Here-Route")

    # Save the output map and do not open it
    html_path = vis.render(open_browser=False, read_only=False)
