#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:13:21 2020

@author: ikespand
"""

# import sys
# sys.path.append("..")
from rasta.gpx import GpxParser


def test_gpx():
    """Tests the Gpx modele against a provided file in tracks"""
    gpx_instance = GpxParser("./tracks/dmrc.gpx", calculate_distance=True)

    total_dist = gpx_instance.data["distance"].sum()

    assert isinstance(gpx_instance, GpxParser)
    assert round(total_dist, 1) == 56.4
