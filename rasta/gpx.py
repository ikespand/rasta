#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A generalise class for GPX data.

@author: ikespand
"""

import gpxpy
import pandas as pd
import geopandas
import numpy as np
from rasta.process_geo_data import ProcessGeoData
from keplergl_cli.keplergl_cli import Visualize
from shapely.geometry import LineString
import os

# %%


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
        """Function to read GPX file with gpxpy library and then postprocess
        the data.
        """
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
        """If timestamp is available then use it to calculate speed."""
        for i in range(0, len(self.data) - 1):
            self.data.iloc[i + 1, 5] = (
                3600
                * self.data.iloc[i + 1, 4]
                / (self.data.iloc[i + 1, 3] - self.data.iloc[i, 3]).seconds
            )

    def convert_to_linestring(self):
        """Convert the pandas df to linestring."""
        return LineString(
            geopandas.points_from_xy(
                x=self.data.longitude, y=self.data.latitude
            )
        )

    def visualize_route(
        self,
        MAPBOX_API_KEY=None,
        output_map=os.getcwd() + "/_mymap",
        open_browser=False,
        read_only=False,
        config_file=None,
    ):
        """Visualize the GPX route with kepler.gl"""
        # Kepler.gl doesn't work properly if timestamp is not string
        if not self.data["time"].isnull().values.any():
            self.data["time"] = self.data["time"].apply(str)

        # Use keplergl_cli
        gpx_visualize = Visualize(
            api_key=MAPBOX_API_KEY,
            config_file=config_file,
            output_map=output_map,
        )

        gpx_visualize.add_data(data=self.data, names="point data")
        route_osm = self.convert_to_linestring()
        gpx_visualize.add_data(data=route_osm, names="line string")
        html_path = gpx_visualize.render(
            open_browser=open_browser, read_only=read_only
        )
        return html_path, gpx_visualize
