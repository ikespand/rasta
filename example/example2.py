#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example show the usage with a downloaded gpx file for the DMRC route. It
doesn't have the timestamp information. So, we cannot find the speed.

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
# Convert our point data to a line data
total_dist = df["distance"].sum()
route_osm = LineString(geopandas.points_from_xy(x=df.lon, y=df.lat))

# %% Visualize with Kepler
# Kepler needs time as string, otherwise it will throw an error
df["time"] = df["time"].apply(str)

vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map=os.getcwd())

vis.add_data(data=df, names='point data')
vis.add_data(data=route_osm, names='line string')
html_path = vis.render(open_browser=False, read_only=False)
