# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from rasta.gpx import GpxParser
from rasta.rasta_kepler import RastaKepler
import os


def test_gpx():
    gpx_instance = GpxParser("./tracks/dmrc.gpx", calculate_distance=False)
    html_path, vis = gpx_instance.visualize_route(open_browser=False,
                                                  MAPBOX_API_KEY="DummyKey")
    assert isinstance(gpx_instance, GpxParser)
    assert len(gpx_instance.data) == 425
    assert isinstance(vis, RastaKepler)
    assert os.path.splitext(html_path)[1] == ".html"
