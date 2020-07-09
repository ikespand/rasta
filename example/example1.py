#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 22:38:40 2020

@author: ikespand
"""
import sys
sys.path.append( '../../keplergl_cli/' )
sys.path.append( '../rasta/' )
from keplergl_cli.keplergl_cli import Visualize
import os
from shapely.geometry import LineString
import geopandas
from settings import *
from gpx_parser import GpxParser

#%%
# Load the gpx file
gpx_instance = GpxParser("BicyleRoute-July2020.gpx")
df = gpx_instance.data

#%%
# Sometime time doesn't change so we get Inf in avg_speed, so replace them by 0
total_time = (df.iloc[-1,3]-df.iloc[0,3]).seconds/3600 #in hours
total_dist = df["distance"].sum()
average_speed = total_dist/total_time

# average_speed_pandas = df["avg_speed"].mean()

# Average speed of pandas and 
# Convert our point data to a line data
route_osm = LineString(geopandas.points_from_xy(x=df.lon, y=df.lat))

#%% Visualize with Kepler
# Kepler needs time as string, otherwise it will throw an error 
df["time"] = df["time"].apply(str)

vis = Visualize(api_key=MAPBOX_API_KEY, config_file = "keplergl_config.json", output_map = os.getcwd())
vis.add_data(data=df, names='point data')
vis.add_data(data=route_osm, names='line string')
html_path = vis.render(open_browser=True, read_only=False)