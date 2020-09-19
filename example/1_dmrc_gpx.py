#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example demonstrate the usage of `rasta` for a gpx route which has timestamp
information in it. 

@author: ikespand
"""
import os
from settings import *
from keplergl_cli.keplergl_cli import Visualize
from shapely.geometry import LineString
import geopandas
from gpx_parser import GpxParser

# %%
# Load the gpx file
gpx_instance = GpxParser("dmrc.gpx",
                         calculate_distance=True)
# Extract the data
df = gpx_instance.data

# %% Further calculations
total_dist = df["distance"].sum()
# average_speed_pandas = df["avg_speed"].mean()

# Convert our point data to a line data
route_osm = LineString(geopandas.points_from_xy(x=df.lon, y=df.lat))

# %% Visualize with Kepler
vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map=os.getcwd())

vis.add_data(data=df, names='point data')
vis.add_data(data=route_osm, names='line string')
html_path = vis.render(open_browser=False,
                       read_only=False)
