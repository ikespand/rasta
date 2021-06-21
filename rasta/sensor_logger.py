#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:39:16 2020

@author: ikespand
"""

import pandas as pd
from rasta.rasta_kepler import RastaKepler
import geopandas as gpd
import zipfile
import sys

# %%


class SensorLogger:
    """SensorLogger is a mobile app which allow you to record the sensor data
    from your mobile. This app is available for both Android and iOS. After the
    recording, you can parse and visualize the zip file with this module.
    Please note that it is not an official program from SensorLogger team.
    Info: https://www.tszheichoi.com/sensorlogger
    """

    def __init__(
        self,
        zip_file: str,
        read_location: bool = True,
        read_accelerometer: bool = True,
        read_orientation: bool = True,
        sync_with: str = "Location",
        read_sensors: list = [],
    ):
        self.zip_file = zip_file
        self.read_location = read_location
        self.read_accelerometer = read_accelerometer
        self.read_orientation = read_orientation
        self.sync_with = sync_with
        self.read_sensors = read_sensors
        self.data_pipeline()

    def data_pipeline(self):
        """
        Run different functions in a pipeline manner.

        Returns
        -------
        None.

        """
        self.read_zip()
        self.read_from_zip()
        self.get_data_from_zip()
        self.sync_data()

    def read_zip(self):
        """
        Read the zip file containing various csv.

        Returns
        -------
        None.

        """
        self.zf = zipfile.ZipFile(self.zip_file)
        self.filelists = self.zf.namelist()
        print("Available sensor files: {}".format(self.filelists))

    def read_from_zip(self):
        """
        Reads all or only predefined sensor files. We put all dataframes into
        a dictionary with key value corresponds to the sensor name.

        Returns
        -------
        None.

        """
        if not len(self.read_sensors) == 0:
            self.read_sensors = [rs + ".csv" for rs in self.read_sensors]
            __readable_files = [
                rs for rs in self.read_sensors if rs in self.filelists
            ]
            # Always provide metadata
            __readable_files.append("Metadata.csv")
            # It can be possible that users have provided wrong sensor names,
            # therefore explictly print that
            print("Reading only: {}".format(__readable_files))
        else:
            print("Reading all available sensors")
            __readable_files = self.filelists
        # Initialize an empty dictionary which will hold all the data.
        self.sensor_df = {}
        for filelist in __readable_files:
            sensor_name = filelist.split(".csv")[0]
            self.sensor_df[sensor_name] = pd.read_csv(self.zf.open(filelist))
            # Rename time and convert it to timestamp except for Metadata
            if not filelist == "Metadata.csv":
                self.sensor_df[sensor_name]["Timestamp"] = pd.to_datetime(
                    self.sensor_df[sensor_name]["time"]
                )
            # Few columns in different sensor have an identical name, so rename
            if filelist == "Accelerometer.csv":
                self.sensor_df["Accelerometer"].rename(
                    columns={"x": "ac_x", "y": "ac_y", "z": "ac_z"},
                    inplace=True,
                )
            if filelist == "Gyroscope.csv":
                self.sensor_df["Gyroscope"].rename(
                    columns={"x": "gy_x", "y": "gy_y", "z": "gy_z"},
                    inplace=True,
                )
            if filelist == "Gravity.csv":
                self.sensor_df["Gravity"].rename(
                    columns={"x": "gr_x", "y": "gr_y", "z": "gr_z"},
                    inplace=True,
                )
            if filelist == "Magnetometer.csv":
                self.sensor_df["Magnetometer"].rename(
                    columns={"x": "ma_x", "y": "ma_y", "z": "ma_z"},
                    inplace=True,
                )

    def print_metadata(self):
        """
        Print the metadata using pandas and tabulate.

        Returns
        -------
        None.

        """
        print("Metadata of this recording is :")
        print(self.sensor_df["Metadata"].to_markdown())

    def get_data_from_zip(self):
        """
        Function to read csv data from the zip file with pandas. For now, only
        3 sensors are allowed to read viz. GPS, accelerometer abd gyroscope.
        TODO: Remove it bcz `read_from_zip` is available from now on.

        Returns
        -------
        None.

        """
        if self.read_location:
            self.location = pd.read_csv(self.zf.open("Location.csv"))
            self.location["Timestamp"] = pd.to_datetime(self.location["time"])

        if self.read_accelerometer:
            self.accelerometer = pd.read_csv(self.zf.open("Accelerometer.csv"))
            self.accelerometer["Timestamp"] = pd.to_datetime(
                self.accelerometer["time"]
            )
            self.accelerometer.rename(
                columns={"x": "ac_x", "y": "ac_y", "z": "ac_z"}, inplace=True
            )

        if self.read_orientation:
            self.gyroscope = pd.read_csv(self.zf.open("Orientation.csv"))
            self.gyroscope["Timestamp"] = pd.to_datetime(
                self.gyroscope["time"]
            )
            self.gyroscope.rename(
                columns={"x": "gy_x", "y": "gy_y", "z": "gy_z"}, inplace=True
            )

    # def sync_data(self):
    #     """
    #     As the frequency of data capture varies among all sensor, therefore,
    #     this module is to synchronize data to a common timestamp.
    #     TODO: Allow sync with other sensors.

    #     Returns
    #     -------
    #     None.

    #     """
    #     if self.sync_with == "location":
    #         if self.read_accelerometer:
    #             self.location = SensorLogger.sync_sensors(
    #                 self.location, self.accelerometer
    #             )
    #             self.location = self.location.drop(
    #                 ["time_x", "time_y"], axis=1
    #             )

    #         if self.read_orientation:
    #             self.location = SensorLogger.sync_sensors(
    #                 self.location, self.gyroscope
    #             )
    #     else:
    #         print("Sorry! Other methods are not implemented yet.")

    def sync_data(self):
        """
        As the frequency of data capture varies among all sensor, therefore,
        this module is to synchronize data to a common timestamp.

        Returns
        -------
        None.

        """
        if self.sync_with == "Location":
            __sensors = list(self.sensor_df.keys())
            if not (self.sync_with in __sensors):
                print(
                    "Sensor `{}` with which you want to sync other sensors `{}` is not available".format(
                        self.sync_with, __sensors
                    )
                )
                print("Check the spelling or availability and retry!")
                sys.exit()
            __sensors.remove("Metadata")
            __sensors.remove(self.sync_with)
            self.synched = self.sensor_df[self.sync_with].copy()
            for sensor in __sensors:
                print("Synching {} with {}".format(sensor, self.sync_with))
                self.synched = SensorLogger.sync_sensors(
                    self.synched, self.sensor_df[sensor]
                )
        else:
            print("Only sync_with 'Location' is allowed for now!")
            sys.exit()

    @staticmethod
    def sync_sensors(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        tol: pd.Timedelta = pd.Timedelta("0.2 second"),
    ) -> pd.DataFrame:
        """
        Given, 2 dataframes, this module can sync them within a given tolerance
        interval.
        TODO: Provide other methods to interpolate

        Parameters
        ----------
        df1 : pd.DataFrame
            left dataframe.
        df2 : pd.DataFrame
            right dataframe.
        tol : pd.Timedelta, optional
            The default is pd.Timedelta('0.2 second').

        Returns
        -------
        df : pd.DataFrame
            synchronized dataframe.

        """
        df1.index = df1["Timestamp"]
        df2.index = df2["Timestamp"]

        df = pd.merge_asof(
            left=df1,
            right=df2,
            # on = "Timestamp",
            right_index=True,
            left_index=True,
            direction="nearest",
            tolerance=tol,
        )

        df = df.drop(["Timestamp_x", "Timestamp_y"], axis=1)
        df = df.reset_index(drop=False)
        return df

    def save_to_kepler(self, MAPBOX_API_KEY: str, output_map: str = None):
        """
        Write down a map in HTML format using kepler.gl.

        Parameters
        ----------
        MAPBOX_API_KEY : str
            DESCRIPTION. Mapbox API key is necessary for map layers.
        output_map : str, optional
            DESCRIPTION. If given then map will be saved to this location.

        Returns
        -------
        None.

        """
        if output_map is None:
            output_map = self.zip_file.replace(".zip", "-")
        # Kepler.gl needs Timestamp as string only!
        self.synched["Timestamp"] = self.location["Timestamp"].apply(str)
        gdf = gpd.GeoDataFrame(
            self.synched,
            geometry=gpd.points_from_xy(
                self.location.longitude, self.location.latitude
            ),
        )
        # Visuliaze with rasta.kepler
        vis = RastaKepler(
            api_key=MAPBOX_API_KEY,
            output_map=self.zip_file.replace(".zip", ""),
        )
        vis.add_data(data=gdf, names="Sync data")
        vis.render(open_browser=False)


# %%
if __name__ == "__main__":
    import os

    # import matplotlib.pyplot as plt

    # Get MAPBOX API key from environment variable
    MAPBOX_API_KEY = os.environ["MAPBOX_API_KEY"]
    # Instantiate our class with a sample log file from tracks
    my_sensors = SensorLogger(
        zip_file=r"../tracks/2020-11-09_08-17-16.zip",
        sync_with="Location",
        # read_sensors=["Magnetometer", "Location"],
    )
    raw_sensor_dict = my_sensors.sensor_df
    my_sensors.print_metadata()
    my_syched_df = my_sensors.synched
    # # Visualize tracks in map (map witll be saved as an HTML)
    my_sensors.save_to_kepler(MAPBOX_API_KEY)
    # plt.plot(data["ac_x"])
    # plt.plot(data["ac_y"])
    # plt.plot(data["ac_z"])
