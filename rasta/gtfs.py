#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[WIP] Module to process GTFS feed.

@author: ikespand
"""
import pandas as pd
import zipfile
from keplergl_cli.keplergl_cli import Visualize
from shapely.geometry import Point, LineString
import geopandas as gpd

# %%


class Gtfs:
    """GTFS feed parser and visualizer."""

    def __init__(self, zip_file):
        self.fname = zip_file
        self.zf = zipfile.ZipFile(self.fname)
        self.check_required_files()
        self.read_required_files()

    def check_required_files(self):
        """GTFS protocol has certain files which are compulsory and this
        function checks for the same.
        """
        required_files = [
            "agency.txt",
            "stops.txt",
            "routes.txt",
            "trips.txt",
            "stop_times.txt",
        ]
        if set(required_files).issubset(self.zf.namelist()):
            print("All required files for GTFS are available")
        else:
            print("Error. Required files are not available. Exiting..")

    def read_required_files(self):
        """Function to read FEW of the required files of GTFS"""
        self.stops = pd.read_csv(self.zf.open("stops.txt"))
        self.routes = pd.read_csv(self.zf.open("routes.txt"))
        self.trips = pd.read_csv(self.zf.open("trips.txt"))

    def visualize_route(self, MAPBOX_API_KEY, output_map=None):
        """Function to enable a visualization"""
        if output_map is None:
            self.output_map = "Unknown_"
        else:
            self.output_map = output_map
        if not ("shapes.txt" in self.zf.namelist()):
            print("Shape file is not present!")
            # self.visualize_stops(MAPBOX_API_KEY)
            Gtfs.visualizer(
                {"stops": self.stops}, MAPBOX_API_KEY, self.output_map
            )
        else:
            print("Shape file is present, processing...")
            self.process_shapes(MAPBOX_API_KEY)

    @staticmethod
    def visualizer(data, MAPBOX_API_KEY, output_map):
        """Static function which simply usage keplergl_cli to add the data
        to the map.
        """
        vis = Visualize(api_key=MAPBOX_API_KEY, output_map=output_map)
        for key in data:
            vis.add_data(data=data[key], names=key)
        html_path = vis.render(open_browser=False, read_only=False)
        return html_path

    def process_shapes(self, MAPBOX_API_KEY):
        """Here, we find the shape_id from the shapes.txt and then with that
        filter out the route_id and create a geopandas df for each route.
        """
        self.shapes = pd.read_csv(self.zf.open("shapes.txt"))
        if (self.shapes).empty:
            print("Shape file is present, however empty!")
            self.visualize_stops(MAPBOX_API_KEY)
        else:
            shape_ids = self.shapes["shape_id"].unique()
            geo_df = []
            for shape_id in shape_ids:
                # Filter out the shape for given `shape_id`
                shape = self.shapes[self.shapes["shape_id"] == shape_id]
                # Find the trip by matching `shape_idz
                trip = self.trips[self.trips["shape_id"] == shape_id]
                # Find the `route` from the given route_id from the `trip`
                route = self.routes[
                    self.routes["route_id"] == trip["route_id"].unique()[0]
                ]
                route = route.reset_index(drop=True)
                # zip the coordinates into shapely points and convert to gdf
                geometry = [
                    Point(xy)
                    for xy in zip(shape.shape_pt_lon, shape.shape_pt_lat)
                ]
                __df = pd.DataFrame()
                __df.loc[0, "shape_id"] = shape_id
                # Concat the route info to the shape for tooltip in map
                __df1 = pd.concat([__df, route], axis=1)
                # Append for each route
                geo_df.append(
                    gpd.GeoDataFrame(__df1, geometry=[LineString(geometry)])
                )
            self.shape_route = pd.concat(geo_df)
            # self.visualize_routes(shape_route, MAPBOX_API_KEY)

            data = {"stops": self.stops, "shape": self.shape_route}
            Gtfs.visualizer(data, MAPBOX_API_KEY, self.output_map)

    def export_route(self, exported_fname="Unkown_gtfs"):
        self.shape_route.to_file(exported_fname + ".geojson", driver="GeoJSON")


# %%

if __name__ == "__main__":
    # Import MAPBOX_API. Otherwise, paste it here directly
    from settings import MAPBOX_API_KEY

    my_gtfs = Gtfs("../tracks/GTFS_delhi.zip")
    # To use the visulization, user must have a mapbox api key
    # this is free and can be created by going to their website
    my_gtfs.visualize_route(MAPBOX_API_KEY, "Delhi_gtfs_")
    my_gtfs.export_route("Delhi_gtfs")
