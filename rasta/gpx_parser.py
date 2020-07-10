#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 22:53:36 2020

@author: ikespand
"""

import gpxpy
import pandas as pd
import os
import math
import geopandas
import numpy as np

class GpxParser():
    """Class to parse XML based GPS data recordings in gpx format. 
    Additionally, helper function allows postprocessing the data.
    """
    def __init__(self, gpx_file_name, calculate_distance = True):
        self.gpx_file_name = gpx_file_name
        self.R = 6371 # Radius of Earth in km
        self.data = self.gpx_parser()
        if calculate_distance:
            self.data["distance"] = 0.0
            self.data["speed"] = 0.0
            self.get_distance_from_df()
            self.data.iloc[:,5] = self.data.iloc[:,5].replace(np.inf, 0)            
        
    def gpx_parser(self):
        # Load the gpx file
        self.gpx_file = open(self.gpx_file_name, 'r')
        self.gpx = gpxpy.parse(self.gpx_file)
        # Extract the data
        self.data = self.gpx.tracks[0].segments[0].points
        self.df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
        for point in self.data:
            self.df = self.df.append({'lon': point.longitude, 
                                      'lat' : point.latitude, 
                                      'alt' : point.elevation, 
                                      'time' : point.time}, ignore_index=True)
        return self.df
    
    def get_distance_from_df(self):
        # Find the approx distance from the GPS
        for i in range (0, len(self.data)-1):
            self.data.iloc[i+1,4] = self.calculate_distance(self.data["lat"][i], self.data["lon"][i], 
                          self.data["lat"][i+1], self.data["lon"][i+1])
            self.data.iloc[i+1,5] = 3600*self.data.iloc[i+1,4]/(self.data.iloc[i+1,3]-self.data.iloc[i,3]).seconds

    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Using the haversine formula, which is good approximation even at small distances
        # unlike the Shperical Law of Cosines. This method has ~0.3% error built in.
        
        dLat = math.radians(float(lat2) - float(lat1))
        dLon = math.radians(float(lon2) - float(lon1))
        lat1 = math.radians(float(lat1))
        lat2 = math.radians(float(lat2))
    
        a = math.sin(dLat/2) * math.sin(dLat/2) +  math.cos(lat1) * math.cos(lat2) * math.sin(dLon/2) * math.sin(dLon/2)
    
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
        d = self.R * c

        return d    