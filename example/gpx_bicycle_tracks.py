#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example show the usage with a recorded track from mobile. It has the
timestamp information. So, we can also find the speed.

@author: ikespand
"""
import os
from rasta.gpx import GpxParser

# Following just holds the MAPBOX_API_KEY. You can paste it here directly or
# can paste it into your bashrc file and import it from there.
from settings import MAPBOX_API_KEY

# %%
# Load the gpx file
gpx_fname = "../tracks/BicyleRoute.gpx"

gpx_instance = GpxParser(gpx_fname, calculate_distance=True)
# Extract our data in dataframe (df)
df = gpx_instance.data
# Further calculation
total_time = (df.iloc[-1, 3] - df.iloc[0, 3]).seconds / 3600  # in hours
total_dist = df["distance"].sum()
average_speed = total_dist / total_time

# To visualize with Kepler
# If provide, map path should be absolute location.
map_fname = os.path.join(
    os.getcwd() + os.path.splitext(os.path.basename(gpx_fname))[0]
)

# Visaulize the tracks
html_path, vis = gpx_instance.visualize_route(
    MAPBOX_API_KEY=MAPBOX_API_KEY,
    output_map=map_fname,
    open_browser=True,
)

# We can import the configuration file and modify it as per our taste.
# vis.map
# with open("hex_config.py", "w") as f:
#     f.write("config = {}".format(vis.map))
