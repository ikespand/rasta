# rasta
[![PyPI Latest Release](https://img.shields.io/pypi/v/rasta.svg)](https://pypi.org/project/rasta/) [![PyTest](https://github.com/ikespand/rasta/workflows/PyTest/badge.svg)](https://github.com/ikespand/rasta/actions?query=workflow%3APyTest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Python 3.6+](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![Python 3.7+](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 3.8+](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

[![](https://raw.githubusercontent.com/ikespand/rasta/master/docs/Rasta_logo.png)](rasta_logo)

Rasta (rāstā) is a Python based library specifically design to handle geospatial data especially in the context of navigation. Currently, one can use rasta to parse/process/visualize GPX, GTFS, GEOJSON data. In addition, there are modules to use REST API from HERE and OpenTripPlanner for the navigation. 


## Features

-   Parse GPX file and convert them to pandas dataframe in a single line of code. Finally able to visualize the tracks with kepler.gl based interactive map.
- Parse GTFS feed and visualize the network.
-  Navigate with HERE Maps or OpenTripPlanned by using their respective REST APIs.

## Install
Directly install from PyPI:
```
pip install rasta
```
Alternatively, clone this repo and install:
```
git clone https://github.com/ikespand/rasta.git
cd rasta
python setup.py install
```

To visualize data with the kepler.gl, user needs to have Mapbox API key which provides the tiles. Go to [Mapbox.com](https://account.mapbox.com/access-tokens) to get an API key.

## Usage
There are many examples available in the example folder. Additionally, code is documented with docstrings.
### Using GPX tracks
Examples [gpx_bicycle_tracks.py](https://github.com/ikespand/rasta/blob/master/example/gpx_bicycle_tracks.py "`gpx_bicycle_tracks.py`") and [gpx_dmrc_yellow_line.py](https://github.com/ikespand/rasta/blob/master/example/gpx_dmrc_yellow_line.py "gpx_dmrc_yellow_line.py") show the usage of `gpx` module for parsing gpx file along with the data processing. For any generic GPX file:
```python
from rasta.gpx import GpxParser
# Load the gpx file (if timestamp is available then also calculate speed)
gpx_instance = GpxParser("../tracks/BicyleRoute.gpx", calculate_distance=True)
# Extract our data in a dataframe
df = gpx_instance.data
# Visaulize the tracks (You will need Mapbox API key for this step)
html_path, vis = gpx_instance.visualize_route(MAPBOX_API_KEY=MAPBOX_API_KEY,open_browser=True)
```
### Using GTFS feed
Example [gtfs_sample_london.py ](https://github.com/ikespand/rasta/blob/master/example/gtfs_sample_london.py "gtfs_sample_london.py ")is to have the visalization of GTFS feed from a given zip file. For a generic GTFS feed:
```python
from rasta.gtfs import Gtfs
# Parse our GTFS feed
my_gtfs = Gtfs("../tracks/gtfs_london.zip")
# Visaulize the routes (You will need Mapbox API key for this step)
my_gtfs.visualize_route(MAPBOX_API_KEY, "london")
```
### Interaction with REST API of OpenTripPlanner
[otp_visualize_from_rest.ipynb ](https://github.com/ikespand/rasta/blob/master/example/otp_visualize_from_rest.py "otp_visualize_from_rest.ipynb ") is a notebook to demonstrate the usage of  OpenTripPlanner's REST API with rasta. Let's say OTP server is ruuning then one could use:
```python
from navigate_with_otp import GetOtpRoute
import pandas as pd
import numpy as np
# Pass arguments for our query along with parameters for visulization
my_otp_nav = GetOtpRoute(start_coord="28.658420, 77.230757", end_coord="28.544442, 77.206334", MAPBOX_API_KEY=MAPBOX_API_KEY, output_map_path="temporary_map", viz=False)
my_otp_nav.address
gdf, html_path = my_otp_nav.extract_itinerary()
```
## Troubleshooting and some hints
- With keplergl>0.2.1 auto-centering for map data is not working (i.e. you will see San Frasnico as default). Therefore, if you face this issue then consider to downgrade to v0.2.0.
- Sometime, the issue of geopandas, fiona and GDAL appears due to some inter-dependencies. To mitigate it, simply uninstall all 3 and [use conda forge to install geopandas](https://geopandas.org/install.html#using-the-conda-forge-channel "use conda forge to install geopandas").
- If you are new to OTP, then try using docker solution which is documented [here](https://ikespand.github.io/posts/OpenTripPlanner/ "here").

## TODO
- Support for OpenStreetMap data coming from overpy
- GTFS validator
- More tests
- Extend documentation

**Developed at:**
![KLabs_logo](https://raw.githubusercontent.com/ikespand/rasta/master/docs/KLabs_logo.JPG)
