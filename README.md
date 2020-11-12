# rasta

Rasta (rāstā) is a Python based library specifically design to handle geospatial data especially in the context of navigation. Currently, one can use rasta to parse/process/visualize GPX, GTFS, GEOJSON data. In addition, there are modules to use HERE map or OpenTripPlanner's REST API for the navigation. 

## Features

-   Parse gpx file and convert them to pandas dataframe in a single line of code. Finally visualize the tracks with kepler.gl based interactive map.
- Parse GTFS feed and visualize the network [Coming soon: GTFS validator]
-  Navigate with HERE Maps or OpenTripPlanned by using their respective REST APIs.

## Install
Directly install from PyPI:
```
pip install rasta
```

To visualize data with the kepler.gl, user needs to have Mapbox API key which provides the tiles.  Go to [Mapbox.com](https://account.mapbox.com/access-tokens) to get an API key.
Download the `keplergl_cli` from following method because this is customized for our task:
```
pip install git+https://github.com/ikespand/keplergl_cli
```
## Usage
There are many examples available in the example folder. Additionally, code is documented with docstrings.
1. **0_GeoJsonWithKepler.py** demonstrates how easy it is to parse geojson and visualize them [independent of rasta]
2. **1_dmrc_gpx.py** and **2_bicycle_tracks.py** show the usage of rasta.gpx for parsing gpx file along with some data processing
3. **3_visualize_gtfs.py** is to have the visalization of GTFS feed from a given zip file
4. **4_navigate_with_otp.py** is for OpenTripPlanner's rest api.

## TODO
- GTFS validator
- More tests

> Developed @ Kratrim Labs