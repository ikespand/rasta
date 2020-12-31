#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example to demonstrate the usage of Gpx class in rasta which doesn't have the
timestamp. Here, we're providing a custom JSON file to control kepler.gl

@author: ikespand
"""
import os
from rasta.gpx import GpxParser

# %% Main Program
MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]
# MAPBOX_API_KEY = "MY_LONG_MAPBOX_API_KEY"

# Load the gpx file
gpx_instance = GpxParser("../tracks/dmrc.gpx", calculate_distance=True)
# Extract the data
df = gpx_instance.data
# Visaulize the tracks
map_location = gpx_instance.visualize_route(
    MAPBOX_API_KEY=MAPBOX_API_KEY,  # Necessary for this function
    output_map=os.getcwd() + "/dmrc",  # Optional
    open_browser=True,  # Optional
    config_file="keplergl_config_sample.json",  # Optional
)

# Further calculations
total_dist = df["distance"].sum()
