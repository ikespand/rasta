#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example demonstrate the usage of rasta for a gpx route which has timestamp
information in it. 

@author: ikespand
"""
from settings import *
from keplergl_cli.keplergl_cli import Visualize
import os
from shapely.geometry import LineString
import geopandas
from gpx_parser import GpxParser
# %%
# Load the gpx file
gpx_instance = GpxParser("dmrc.gpx",
                         calculate_distance=True)
df = gpx_instance.data

# %% Further calculation
total_dist = df["distance"].sum()
# average_speed_pandas = df["avg_speed"].mean()

# Average speed of pandas and
# Convert our point data to a line data
route_osm = LineString(geopandas.points_from_xy(x=df.lon, y=df.lat))

# %% Visualize with Kepler
# Kepler needs time as string, otherwise it will throw an error

vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map=os.getcwd())

vis.add_data(data=df, names='point data')
vis.add_data(data=route_osm, names='line string')
html_path = vis.render(open_browser=False,
                       read_only=False)
