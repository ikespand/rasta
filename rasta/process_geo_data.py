#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:10:45 2020

@author: ikespand
"""

import math


class ProcessGeoData:
    """Some methods to post process geospatial data"""

    @staticmethod
    def get_distance_from_df(data):
        # Find the approx distance from the GPS
        dist = [0]
        for i in range(0, len(data) - 1):
            d = ProcessGeoData.calculate_distance(
                data["latitude"][i],
                data["longitude"][i],
                data["latitude"][i + 1],
                data["longitude"][i + 1],
            )
            dist.append(d)
        return dist

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Using the haversine formula, which is good approximation even at
        small distances unlike the Shperical Law of Cosines. This method has
        ~0.3% error built in.
        """

        dLat = math.radians(float(lat2) - float(lat1))
        dLon = math.radians(float(lon2) - float(lon1))
        lat1 = math.radians(float(lat1))
        lat2 = math.radians(float(lat2))

        a = math.sin(dLat / 2) * math.sin(dLat / 2) + (
            math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dLon / 2)
            * math.sin(dLon / 2)
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        d = 6371 * c

        return d
