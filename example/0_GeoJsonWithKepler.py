#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This example shows an example in which we will read a geoJson file with the
help of geopandas and extract useful information and visualize with the help
of Kepler.

@author: ikespand
"""
from settings import MAPBOX_API_KEY
from keplergl_cli.keplergl_cli import Visualize
import geopandas as gpd

# %% Geopandas can parse geojson
fname = "../tracks/IITDelhi_roadnetwork.geojson"
geodf = gpd.read_file(fname)
# %% Visualize with Kepler
vis = Visualize(
    api_key=MAPBOX_API_KEY,
    config_file="keplergl_config.json",
    output_map="../tracks/IITDelhi_roads",
)
# Add the data to Visualize
vis.add_data(data=geodf, names="IITD and surroundings")
# Save the output map and do not open it
html_path = vis.render(open_browser=False, read_only=True)
