#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A generalise class for Gpx data.
@author: ikespand
"""

import gpxpy
import pandas as pd
import numpy as np
from process_geo_data import ProcessGeoData


class GpxParser:
    """Class to parse XML based GPS data recordings in gpx format.
    Additionally, helper function allows postprocessing the data.
    """

    def __init__(self, gpx_file_name, calculate_distance=False):
        self.gpx_file_name = gpx_file_name
        self.data = self.gpx_parser()
        if calculate_distance:
            self.EARTH_RADIUS = 6371  # Radius of Earth in km
            # self.data["distance"] = 0.0
            # self.get_distance_from_df()
            self.data["distance"] = ProcessGeoData.get_distance_from_df(
                self.data
            )
            if not self.data["time"].isnull().values.any():
                self.data["speed"] = 0.0
                self.get_speed()
                self.data.iloc[:, 5] = self.data.iloc[:, 5].replace(np.inf, 0)
            else:
                print("No timestamps -> Skipping speed calculation..")

    def gpx_parser(self):
        # Load the gpx file
        self.gpx_file = open(self.gpx_file_name, "r")
        self.gpx = gpxpy.parse(self.gpx_file)
        # Extract the data
        self.data = self.gpx.tracks[0].segments[0].points
        self.df = pd.DataFrame(
            columns=["longitude", "latitude", "altitude", "time"]
        )
        for point in self.data:
            self.df = self.df.append(
                {
                    "longitude": point.longitude,
                    "latitude": point.latitude,
                    "altitude": point.elevation,
                    "time": point.time,
                },
                ignore_index=True,
            )
        return self.df

    def get_speed(self):
        for i in range(0, len(self.data) - 1):
            self.data.iloc[i + 1, 5] = (
                3600
                * self.data.iloc[i + 1, 4]
                / (self.data.iloc[i + 1, 3] - self.data.iloc[i, 3]).seconds
            )
