#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example show the usage with a recorded track from mobile. It has the
timestamp information. So, we can also find the speed.

@author: ikespand
"""
import os
from settings import MAPBOX_API_KEY
from gpx import GpxParser

# %%
# Load the gpx file
gpx_fname = "../tracks/BicyleRoute-July2020.gpx"

gpx_instance = GpxParser(gpx_fname, calculate_distance=True)
# Extract our data in dataframe (df)
df = gpx_instance.data
# %% Further calculation
total_time = (df.iloc[-1, 3] - df.iloc[0, 3]).seconds / 3600  # in hours
total_dist = df["distance"].sum()
average_speed = total_dist / total_time

# Visualize with Kepler
map_fname = os.path.splitext(os.path.basename(gpx_fname))[0]

# Visaulize the tracks
html_path, vis = gpx_instance.visualize_route(
    mapbox_api_key=MAPBOX_API_KEY,
    output_map=map_fname,
    open_browser=True,
)

# %% Save the configuration of map for future usage

# vis.map
# with open("hex_config.py", "w") as f:
#     f.write("config = {}".format(vis.map))
