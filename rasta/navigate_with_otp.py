#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 20:32:41 2020

@author: ikespand
"""
import geopandas as gpd
import pandas as pd
import requests
from keplergl_cli.keplergl_cli import Visualize
import polyline
import datetime
from shapely.geometry import LineString

# %%


class GetOtpRoute:
    """Navigation with OpenTripPlanner"""

    def __init__(
        self,
        start_coord,
        end_coord,
        viz=True,
        MAPBOX_API_KEY=None,
        output_map_path="navigation_with_otp",
    ):
        self.src = start_coord
        self.tgt = end_coord
        self.base_address = "http://localhost:8080/otp/routers/default"
        self.get_routes()
        self.mapbox_api_key = MAPBOX_API_KEY
        self.output_map_path = output_map_path
        # self.extract_itinerary()

    def build_query(self):
        """Update the query"""
        self.address = (
            self.base_address
            + "/plan?fromPlace="
            + self.src
            + "&toPlace="
            + self.tgt
        )

    def get_routes(self):
        """From the built query, inquire the api of otp"""
        self.build_query()
        self.response = requests.get(
            self.address, headers={"Accept-type": "application/json"}
        )

        if self.response.status_code == 200:
            self.response_json = self.response.json()
            # pprint(response_json)
        elif self.response.status_code == 404:
            print("ERROR")
            # Exit

    def extract_itinerary(self):
        """Function to extract only the irineraries"""
        vis = Visualize(
            api_key=self.mapbox_api_key, output_map=self.output_map_path
        )
        gdf = []
        for i in range(0, len(self.response_json["plan"]["itineraries"])):
            itinerary = self.response_json["plan"]["itineraries"][i]
            vis, df = GetOtpRoute.plot_itinerary(vis, itinerary, i)
            gdf.append(df)
        html_path = vis.render(open_browser=False, read_only=True)
        return gdf, html_path

    @staticmethod
    def plot_itinerary(vis, itinerary, i):
        """To add a visualization in kepler.gl"""
        gdf = []
        for k in range(0, len(itinerary["legs"])):
            leg = itinerary["legs"][k]
            gdf.append(GetOtpRoute.extract_from_a_leg(leg))
            # Add the data to Visualize
        gdf = pd.concat(gdf)
        vis.add_data(data=gdf, names="Itinerary{}_Route{}".format(i, k))
        return [vis, gdf]

    @staticmethod
    def extract_from_a_leg(leg):
        """Returns a gdf with for a given travel leg within an internary"""
        leg_mode = leg["mode"]

        start_time = leg["startTime"]
        start_time = datetime.datetime.fromtimestamp(start_time / 1e3)

        end_time = leg["endTime"]
        end_time = datetime.datetime.fromtimestamp(end_time / 1e3)

        leg_geometry = polyline.decode(
            leg["legGeometry"]["points"], geojson=True
        )

        distance = leg["distance"]
        duration = leg["duration"]

        gdf = gpd.GeoDataFrame(
            {
                "leg_mode": [leg_mode],
                "start_time": str(start_time),
                "end_time": str(end_time),
                "distance": distance,
                "duration": duration,
            },
            geometry=[LineString(leg_geometry)],
        )
        return gdf


# %%
if __name__ == "__main__":
    from settings import MAPBOX_API_KEY  # THIS HOLDS API KEYS

    my_otp_nav = GetOtpRoute(
        start_coord="28.69782,77.19269",
        end_coord="28.60743,77.22702",
        MAPBOX_API_KEY=MAPBOX_API_KEY,
        output_map_path="temporary_map_",
    )

    gdf, html_path = my_otp_nav.extract_itinerary()
