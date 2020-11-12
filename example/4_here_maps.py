#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script usage the HERE MAPS API to determine the fastest public transit
route. Further, we use data from any custom 3rd party BIKE_STATION and with
some more post processing we recommend an optimum path.

This can act as rest api which will return geojson data for available options.

"""

import geopandas as gpd

# import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point, LineString
from settings import *  # THIS HOLDS API KEYS
from keplergl_cli.keplergl_cli import Visualize
from navigate_with_here import GetHereRoute
from process_geo_data import ProcessGeoData
import numpy as np

# %% INPUTS

start_coord = "12.873132,77.661479"  # Should come from the request
end_coord = "12.877664,77.665843"  # Should come from the request

WALKING_SPEED = 5
BICYLCE_SPEED = 15
PROCESS_BIKE_STATION = False

BIKE_STATION = [(12.973007, 77.602306)]  # START WITH DUMMY STATION
if PROCESS_BIKE_STATION:
    BIKE_STATION = pd.read_excel(
        "../../Data_Blore/BIKE_STATION/BIKE_STATION Jan 2020.xlsx", "Sheet1", nrows=100
    )

    BIKE_STATION = []
    for j in range(0, len(BIKE_STATION)):
        BIKE_STATION.append(
            (BIKE_STATION["start latitude"][j], BIKE_STATION["start longitude"][j])
        )


# %%
def find_nearby_bike_station(lat, lon, BIKE_STATION, R=0.1):
    """Check if there is a nearby BIKE_STATION station. This station should be within
    30% of walking distance. E.g. if walking distance to metro station is 1 km
    then this station should be maximum 300 m away (CUSTOM RULE).
    """
    for y in BIKE_STATION:
        r = ProcessGeoData.calculate_distance(lat, lon, y[0], y[1])
        BIKE_STATION_available = False
        BIKE_STATION_location = []
        if r <= R:
            BIKE_STATION_available = True
            BIKE_STATION_location = (y[0], y[1])
            break
    return [BIKE_STATION_available, BIKE_STATION_location]


# %% Get data from HERE with the help of written class in rasta


start_coord = "12.874132,77.661479"  # Should come from the request
end_coord = "12.877664,77.665843"  # Should come from the request

my_here_route = GetHereRoute(start_coord, end_coord, HERE_API_KEY)
json_data = my_here_route.json_data
nav_data = my_here_route.nav_data_df
# nav_data.to_csv("nav.csv", index=False)

# %% Process the route for custom operations
# ASSUMING ONLY 3 LEGS: PRIVATE > PUBLIC > PRIVATE
gdf_nav = []
pt = []
for k in range(0, len(nav_data)):
    dist = nav_data["distance"][k]
    if (nav_data["type"][k] == "PrivateTransportManeuverType") and (
        nav_data["distance"][k] > 0.5
    ):
        _, bike_stn_loc = find_nearby_bike_station(
            12.973132,
            77.601479,
            BIKE_STATION=BIKE_STATION,
            R=0.3 * nav_data["distance"][k],
        )
    pt.append((nav_data.loc[k].longitude, nav_data.loc[k].latitude))

    # __gdf = gpd.GeoDataFrame(nav_data.loc[[k]],geometry=[Point(pt[k])])
    if k != 0:
        __gdf = gpd.GeoDataFrame(
            nav_data.loc[[k]],
            crs="EPSG:4326",
            geometry=[LineString([Point(pt[k - 1]), Point(pt[k])])],
        )

    else:
        __gdf = gpd.GeoDataFrame(nav_data.loc[[k]], geometry=[Point(pt[k])])

    gdf_nav.append(__gdf)
gdf_nav = pd.concat(gdf_nav)
gdf_123 = gdf_nav.reset_index(drop=True)
# %%
# Some heaurstics
gdf_123["price"] = 0
gdf_123["time"] = 0

for i in range(0, len(gdf_123)):
    if gdf_123["type"][i] == "PrivateTransportManeuverType":
        if gdf_123["distance"][i] <= 0.8:
            gdf_123["type"][i] = "Walk"
            gdf_123["price"][i] = 0
            gdf_123["time"][i] = 60 * gdf_123["distance"][i] / WALKING_SPEED
        elif (gdf_123["distance"][i] > 0.8) and (gdf_123["distance"][i] <= 2):
            gdf_123["type"][i] = "BIKE_STATION"
            gdf_123["price"][i] = 10 + 15
            gdf_123["time"][i] = 60 * gdf_123["distance"][i] / BICYLCE_SPEED
        else:
            gdf_123["type"][i] = "Uber"
            gdf_123["price"][i] = 45 + (gdf_123["distance"][i] * 6)
            gdf_123["time"][i] = gdf_123["distance"][i] / 40
    elif gdf_123["type"][i] == "PublicTransportManeuverType":
        gdf_123["type"][i] = "PublicTransport"
        gdf_123["price"][i] = 15
        gdf_123["time"][i] = 60 * gdf_123["distance"][i] / 60


# gdf_123.to_file("output.json", driver="GeoJSON")
# %% Visualize with Kepler

vis = Visualize(
    api_key=MAPBOX_API_KEY,
    config_file="keplergl_config.json",
    output_map="Optimum_here",
)
# Add the data to Visualize
vis.add_data(data=gdf_123, names="Route-1")

# Save the output map and do not open it
html_path = vis.render(open_browser=False, read_only=False)

# %% SUMMARY FOR DEBUGGING
# Replace RENTAL BIKE with Walk to have this as an option
gdf_123_o1 = gdf_123.copy()
gdf_123_o1["price"][gdf_123_o1["type"] == "BIKE_STATION"] = 0
gdf_123_o1["type"][gdf_123_o1["type"] == "BIKE_STATION"] = "Walk"

print("------------------################--------------------------")
print("------------------Option-1--------------------------")
print("Total price for this journey", np.sum(gdf_123["price"]), "rupees")
print("Total distance travelled", np.sum(gdf_123["distance"]), "km")
print(
    "Total walking distance",
    np.sum(gdf_123["distance"][gdf_123["type"] == "Walk"]),
    "km",
)
print(
    "You can save ",
    np.sum(gdf_123["distance"][gdf_123["type"] != "Uber"]) * 130,
    "gram of CO2 by using our suggested route!",
)
print("------------------Option-2--------------------------")
print("Total price for this journey", np.sum(gdf_123_o1["price"]), "rupees")
print("Total distance travelled", np.sum(gdf_123_o1["distance"]), "km")
print(
    "Total walking distance",
    np.sum(gdf_123_o1["distance"][gdf_123_o1["type"] == "Walk"]),
    "km",
)
print(
    "You can save ",
    np.sum(gdf_123_o1["distance"][gdf_123_o1["type"] != "Uber"]) * 130,
    "gram of CO2 by using our suggested route!",
)
print("------------------################--------------------------")
