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
import shapely.wkt
#%%
#APIKEY= "Bearer a559433c8d2d91b2329f24457b6dc122"
#address = "https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals?lat=48.780816&lon=9.201172&radius=2000&limit=4&providernetwork=2"
#response = requests.get(address, headers={"Authorization":APIKEY})
#
#aa=response.json()
#%%

def navigate_me(start_coord="48.758200, 9.269780", end_coord="48.780816, 9.201172"):
    address= "http://localhost:8080/otp/routers/default/plan?fromPlace="+start_coord+"&toPlace="+end_coord
    response = requests.get(address, headers={"Accept-type":"application/json"})

    if response.status_code == 200:
        response_json = response.json()
        #pprint(response_json)
        return response_json
    elif response.status_code == 404:
        print("ERROR")
        return 404
    return None

def extract_itinerary(response_json):
    vis = Visualize(api_key=MAPBOX_API_KEY,
                    config_file="keplergl_config.json",
                    output_map="OTP-0")
    gdf =[]
    for i in range(0, len(response_json["plan"]["itineraries"])):
        itinerary = response_json["plan"]["itineraries"][i]
        vis, df = plot_itinerary(vis, itinerary, i)
        gdf.append(df)
    html_path = vis.render(open_browser=False, read_only=False)
    return gdf

def extract_from_a_leg(leg):    
    leg_mode = leg["mode"]
    
    start_time = leg["startTime"]
    start_time = datetime.datetime.fromtimestamp(start_time / 1e3)
    
    end_time = leg["endTime"]
    end_time = datetime.datetime.fromtimestamp(end_time / 1e3)
    
    leg_geometry = polyline.decode(leg["legGeometry"]["points"], geojson=True)

    distance = leg["distance"]
    duration = leg["duration"]

    
    gdf = gpd.GeoDataFrame({"leg_mode":[leg_mode],
                            "start_time":str(start_time),
                            "end_time":str(end_time),
                            "distance":distance,
                            "duration": duration},
                            geometry = [LineString(leg_geometry)])
    return gdf

def plot_itinerary(vis, itinerary, i):
    gdf = []
    for k in range (0, len(itinerary["legs"])):
        leg = itinerary["legs"][k]
        gdf.append(extract_from_a_leg(leg)) 
        # Add the data to Visualize
    gdf = pd.concat(gdf)
    vis.add_data(data=gdf, names='Itinerary{}_Route{}'.format(i,k))
    return [vis, gdf]
#%%     
response_json = navigate_me(start_coord="48.701248, 9.037058", end_coord="48.780816, 9.201172")
df=extract_itinerary(response_json)    

#%%
#leg_from_lat = leg["from"]["lat"]
#leg_from_lon = leg["from"]["lon"]
#leg_to_lat = leg["to"]["lat"]
#leg_to_lon = leg["to"]["lon"]
#
#df = pd.DataFrame()
#df["leg_from_lat"] = [leg_from_lat]
#df["leg_from_lon"] = [leg_from_lon]
#df["leg_to_lat"] = [leg_from_lat]
#df["leg_to_lon"] = [leg_from_lon]
#gdf.to_file("output.json", driver="GeoJSON")
