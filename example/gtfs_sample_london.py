#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process and visualize GTFS feed with the help of `gtfs` module in `rasta`.

@author: ikespand
"""
from rasta.gtfs import Gtfs
import os

# %%
MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]
# MAPBOX_API_KEY = "MY_LONG_MAPBOX_API_KEY"
my_gtfs = Gtfs("../tracks/gtfs_london.zip")
# To use the visulization, user must have a mapbox api key
# this is free and can be created by going to their website
my_gtfs.visualize_route(MAPBOX_API_KEY, "london_can")
