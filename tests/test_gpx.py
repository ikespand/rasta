# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from rasta.process_geo_data import ProcessGeoData


def test_calculate_distance():
    lat1, lon1 = 48.753435, 9.181379
    lat2, lon2 = 48.748685, 9.186582
    straigh_line_distance = ProcessGeoData.calculate_distance(
        lat1, lon1, lat2, lon2
    )

    assert round(straigh_line_distance, 2) == 0.65
