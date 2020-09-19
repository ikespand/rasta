"""
Copyright (C) 2020 Kratrim Labs - All Rights Reserved

This script usage the HERE MAPS API to determine the fastest public transit 
route. Further, we use data from Yulu station and with some more post processing
we recommend an optimum path.

This will act as rest api which will return geojson data for (upto) 3 available options.

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

#%% INPUTS
start_coord = "12.873132,77.661479"  # Should come from the request
end_coord = "12.877664,77.665843"  # Should come from the request

WALKING_SPEED = 5
BICYLCE_SPEED = 15
PROCESS_YULU = False

YULU = [(12.973007,77.602306)] # START WITH DUMMY STATION
if PROCESS_YULU:
    yulu = pd.read_excel("../../Data_Blore/Yulu/Yulu Jan 2020.xlsx","Sheet1", nrows=100)
    
    YULU = []
    for j in range(0, len(yulu)):
        YULU.append((yulu["start latitude"][j],yulu["start longitude"][j]))
        

#%%s
class ProcessGeoData():
    """Some methods to post process geospatial data"""
    @staticmethod
    def get_distance_from_df(data):
        # Find the approx distance from the GPS
        for i in range(0, len(data) - 1):
            data.iloc[i+1, 4] = ProcessGeoData.calculate_distance(data["latitude"][i],
                                      data["longitude"][i],
                                      data["latitude"][i+1],
                                      data["longitude"][i+1])
    @staticmethod    
    def calculate_distance(lat1, lon1, lat2, lon2):
        """ Using the haversine formula, which is good approximation even at
        small distances unlike the Shperical Law of Cosines. This method has
        ~0.3% error built in.
        """
    
        dLat = math.radians(float(lat2) - float(lat1))
        dLon = math.radians(float(lon2) - float(lon1))
        lat1 = math.radians(float(lat1))
        lat2 = math.radians(float(lat2))
    
        a = math.sin(dLat/2) * math.sin(dLat/2) + \
            math.cos(lat1) * math.cos(lat2) * math.sin(dLon/2) * \
            math.sin(dLon/2)
    
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
        d = 6371 * c
    
        return d

def find_nearby_yulu(lat, lon, YULU, R=0.1):
    """Check if there is a nearby Yulu station. This station should be within
    30% of walking distance. E.g. if walking distance to metro station is 1 km
    then this station should be maximum 300 m away (CUSTOM RULE).
    """
    for y in YULU:
        r = ProcessGeoData.calculate_distance(lat, lon, y[0], y[1])
        yulu_available = False
        yulu_location = []
        if r <=R:
            yulu_available = True
            yulu_location = (y[0], y[1])
            break
    return [yulu_available, yulu_location]
#%% Get data from HERE 
    
class get_here_route():
    """It should hold all modules for here map.
    """
    pass

address= "https://route.ls.hereapi.com/routing/7.2/calculateroute.json?apiKey="+here_api+"&waypoint0=geo!"+start_coord+"&waypoint1=geo!"+end_coord+"&departure=now&mode=fastest;publicTransport&combineChange=true"

response = requests.get(address)

if response.status_code == 200:
    print('Success!')
elif response.status_code == 404:
    print('Not Found.')

#%% Data extraction
response_json = response.json()
maneuver_type = []
coordinate_lat = []
coordinate_lon = []
instruction = []
for k in response_json["response"]["route"][0]["leg"][0]["maneuver"]:
    #print(k["_type"])
    maneuver_type.append(k["_type"])
    coordinate_lat.append(k["position"]["latitude"])
    coordinate_lon.append(k["position"]["longitude"])
    instruction.append(k["instruction"])

#%%
nav_data = pd.DataFrame()
nav_data["type"] = maneuver_type
nav_data["latitude"] = coordinate_lat
nav_data["longitude"] = coordinate_lon
nav_data["instruction"] = instruction
nav_data["distance"] = 0.0
ProcessGeoData.get_distance_from_df(nav_data)
#nav_data = nav_data[nav_data["type"]=="PublicTransportManeuverType"]
#nav_data.to_csv("nav.csv", index=False)

#%%
#grouped_nav1=nav_data.groupby((nav_data.type!=nav_data.type.shift()).cumsum())
#groups = sorted(grouped_nav1)
#grouped_nav = [g for _, g in groups]
nav_data["distance"].sum()
#%%
# ASSUMING ONLY 3 LEGS: PRIVATE > PUBLIC > PRIVATE
#grouped_nav=[list(group) for key, group in groupby(nav_data.type.values.tolist())]

#%%
gdf_nav = []
pt = []
for k in range(0, len(nav_data)):
    print("-----",k,"------")
    dist = nav_data["distance"][k]
    if ((nav_data["type"][k] == "PrivateTransportManeuverType") and (nav_data["distance"][k] >0.5)):
         _, yulu_loc = find_nearby_yulu(12.973132,77.601479,
                                        YULU=YULU,
                                        R=.3*nav_data["distance"][k])
    pt.append((nav_data.loc[k].longitude,
               nav_data.loc[k].latitude))

   # __gdf = gpd.GeoDataFrame(nav_data.loc[[k]],geometry=[Point(pt[k])])
    if k!=0:
        __gdf = gpd.GeoDataFrame(nav_data.loc[[k]], crs="EPSG:4326",
                                 geometry=[LineString([Point(pt[k-1]), Point(pt[k])])])
        
    else:
        __gdf = gpd.GeoDataFrame(nav_data.loc[[k]],
                                 geometry=[Point(pt[k])])

    gdf_nav.append(__gdf)
    # TODO: Implement routing from start point to Yulu station and then from 
    # there to end point. Similarly check for end point.
#%%
gdf_nav = pd.concat(gdf_nav)
    
gdf_123 = gdf_nav.reset_index(drop=True)

##%% TIME
#gdf_123["walk_time"] = np.where(gdf_123["type"]=="PrivateTransportManeuverType", 60*gdf_123["distance"]/WALKING_SPEED/50, 0) 
#gdf_123["bicycle_time"] = np.where(gdf_123["type"]=="PrivateTransportManeuverType",  60*gdf_123["distance"]/BICYLCE_SPEED, 0) 
#gdf_123["uber_time"] = np.where(gdf_123["type"]=="PrivateTransportManeuverType",  gdf_123["distance"]/30, 0) 
#gdf_123["publictransport_time"] = np.where(gdf_123["type"]=="PublicTransportManeuverType", 60*gdf_123["distance"]/50, 0)
#
##%% PRICE
#gdf_123["walk_price"] = np.where(gdf_123["type"]=="PrivateTransportManeuverType", 0, 0) 
#gdf_123["bicycle_price"] = np.where(gdf_123["type"]=="PrivateTransportManeuverType",  10+15, 0) 
#gdf_123["uber_price"] = np.where(gdf_123["type"]=="PrivateTransportManeuverType",  45+(gdf_123["distance"]*6), 0) 
#gdf_123["publictransport_price"] = np.where(gdf_123["type"]=="PublicTransportManeuverType", 15, 0)
gdf_123.__geo_interface__
#%%
gdf_123["price"] = 0
gdf_123["time"] = 0

for i in range(0, len(gdf_123)):
    if gdf_123["type"][i]=="PrivateTransportManeuverType":
        if gdf_123["distance"][i] <= 0.8:
            gdf_123["type"][i] = "Walk"
            gdf_123["price"][i] = 0
            gdf_123["time"][i] = 60*gdf_123["distance"][i]/WALKING_SPEED
        elif (gdf_123["distance"][i] > 0.8) and (gdf_123["distance"][i] <= 2):
            gdf_123["type"][i] = "Yulu"
            gdf_123["price"][i] = 10+15
            gdf_123["time"][i] = 60*gdf_123["distance"][i]/BICYLCE_SPEED
        else:
            gdf_123["type"][i] = "Uber"
            gdf_123["price"][i] = 45+(gdf_123["distance"][i]*6)
            gdf_123["time"][i] = gdf_123["distance"][i]/40
    elif gdf_123["type"][i]=="PublicTransportManeuverType":
        gdf_123["type"][i] = "PublicTransport"
        gdf_123["price"][i] = 15
        gdf_123["time"][i] = 60*gdf_123["distance"][i]/60

    
#gdf_123["cost_function"] = gdf_123["distance"]+gdf_123["price"]

gdf_123.to_file("output.json", driver="GeoJSON")
    
# %% Visualize with Kepler
gdf_123_o1 = gdf_123.copy()
gdf_123_o1["price"][gdf_123_o1["type"]=="Yulu"] =0
gdf_123_o1["type"][gdf_123_o1["type"]=="Yulu"] ="Walk"

#%%
vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map="Optimum_here")
# Add the data to Visualize
vis.add_data(data=gdf_123, names='Route-1')
#vis.add_data(data=gdf_123_o1, names='Route-2')

# Save the output map and do not open it
html_path = vis.render(open_browser=False,
                       read_only=False)

#%% SUMMARY FOR DEBUGGING
print("------------------################--------------------------")
print("------------------Option-1--------------------------")
print("Total price for this journey",np.sum(gdf_123["price"]), "rupees")
print("Total distance travelled",np.sum(gdf_123["distance"]), "km")
print("Total walking distance",np.sum(gdf_123["distance"][gdf_123["type"]=="Walk"]), "km")
print("You can save ",np.sum(gdf_123["distance"][gdf_123["type"]!="Uber"])*130,"gram of CO2 by using our suggested route!")
print("------------------Option-2--------------------------")
print("Total price for this journey",np.sum(gdf_123_o1["price"]), "rupees")
print("Total distance travelled",np.sum(gdf_123_o1["distance"]), "km")
print("Total walking distance",np.sum(gdf_123_o1["distance"][gdf_123_o1["type"]=="Walk"]), "km")
print("You can save ",np.sum(gdf_123_o1["distance"][gdf_123_o1["type"]!="Uber"])*130,"gram of CO2 by using our suggested route!")
print("------------------################--------------------------")
