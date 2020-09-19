#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 20:32:41 2020

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
from settings import *  # THIS HOLDS API KEYS
from keplergl_cli.keplergl_cli import Visualize
from pprint import pprint
import polyline
import datetime

#%%
start_coord = "45.51994, -122.63643"  # Should come from the request
end_coord = "45.50430, -122.62236"  # Should come from the request

address= "http://localhost:8080/otp/routers/default/plan?fromPlace="+start_coord+"&toPlace="+end_coord


response = requests.get(address)
pprint(response_json)


if response.status_code == 200:
    print('Success!')
elif response.status_code == 404:
    print('Not Found.')

response_json = response.json()



len_iter = len(response_json["plan"]["itineraries"])
itinerary = response_json["plan"]["itineraries"][2]
leg = itinerary["legs"][1]

def extract_from_a_leg():
    pass

#%%
leg_from_lat = leg["from"]["lat"]
leg_from_lon = leg["from"]["lon"]
leg_to_lat = leg["to"]["lat"]
leg_to_lon = leg["to"]["lon"]

leg_mode = leg["mode"]

start_time = leg["startTime"]
start_time = datetime.datetime.fromtimestamp(start_time / 1e3)

end_time = leg["endTime"]
end_time = datetime.datetime.fromtimestamp(end_time / 1e3)

leg_geometry = polyline.decode(leg["legGeometry"]["points"])
geom = LineString(leg_geometry)

gdf = gpd.GeoDataFrame({'leg_from_lat': [leg_from_lat], 
                   'leg_from_lon': [leg_from_lon], 
                   'leg_mode': [leg_mode]}, geometry = [geom])

#%%
vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map="OTP-0")
# Add the data to Visualize
vis.add_data(data=gdf, names='Route-1')
#vis.add_data(data=gdf_123_o1, names='Route-2')

# Save the output map and do not open it
html_path = vis.render(open_browser=False, read_only=False)
