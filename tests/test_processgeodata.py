#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:13:21 2020

@author: ikespand
"""

# import sys
# sys.path.append("..")
from rasta.process_geo_data import ProcessGeoData
import pytest


def test_calculate_distance():
    lat1, lon1 = 48.753435, 9.181379
    lat2, lon2 = 48.748685, 9.186582
    straigh_line_distance = ProcessGeoData.calculate_distance(
        lat1, lon1, lat2, lon2
    )

    assert round(straigh_line_distance, 2) == 0.65
