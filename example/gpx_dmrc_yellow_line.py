#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example to demonstrate the usage of Gpx class in rasta which doesn't have the
timestamp. Here, we're providing a custom JSON file to control kepler.gl

@author: ikespand
"""
import os
from settings import MAPBOX_API_KEY
from rasta.gpx import GpxParser

# %% Main Program
# Load the gpx file
gpx_instance = GpxParser("../tracks/dmrc.gpx", calculate_distance=True)
# Extract the data
df = gpx_instance.data
# Visaulize the tracks
map_location = gpx_instance.visualize_route(
    MAPBOX_API_KEY=MAPBOX_API_KEY,
    output_map=os.getcwd() + "/_dmrc",
    open_browser=True,
    config_file="keplergl_config.json"
)

# Further calculations
total_dist = df["distance"].sum()
