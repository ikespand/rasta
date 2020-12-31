#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 21:31:19 2020

@author: ikespand
"""

from rasta.gtfs import Gtfs


def test_gtfs():
    my_gtfs = Gtfs("./tracks/gtfs_london.zip")
    assert isinstance(my_gtfs, Gtfs)
    assert len(my_gtfs.stops) > 1
