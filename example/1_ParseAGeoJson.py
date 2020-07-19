#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example shows an example in which we will read a geoJson file with the 
help of geopandas and extract useful information and visualize with the help
of Kepler.

@author: ikespand
"""
from settings import *
from keplergl_cli.keplergl_cli import Visualize
import os
import geopandas as gpd

#%%
fname = "IITDelhi_roadnetwork.geojson"
geodf = gpd.read_file(fname)
# %% Visualize with Kepler
# Kepler needs time as string, otherwise it will throw an error

vis = Visualize(api_key=MAPBOX_API_KEY,
                config_file="keplergl_config.json",
                output_map="IITDelhi_roads")

vis.add_data(data=geodf, names='IITD and surroundings')
html_path = vis.render(open_browser=False,
                       read_only=False)
