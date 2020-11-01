# rasta

Rasta (rāstā) is a Python based library specifically design to handle gps tracks. Currently, one can use to parse/process/visualize GPX, GTFS, GEOJSON data. In addition, there are modules to use HERE map or OpenTripPlanner's REST API for the navigation. 

## Features

-   Parse XML gps routes (gpx) easily and get data in pandas df in a single line of code
- Parse GTFS feed and visualize the network [Coming: GTFS validator]
-   Get the distance of consecutive coordinates and perform calculation of speed (if timestamp is available)
-   Integration with kepler gl allows the creation of interactive map with nice visualization
-  Navigate with HERE or OTP with using their respective APIs.

## Install

**Mapbox API key**: To use kepler gl integration, user will need to provide a Mapbox API key. Go to [Mapbox.com](https://account.mapbox.com/access-tokens)
to get an API key.

This package has dependencies on `geojson`, `shapely`, `geopandas`, `gpx` etc.

```
conda install geojson shapely geopandas -c conda-forge
pip install gpx 
```
Download the `keplergl_cli` from following method because this is customized for our task:
```
pip install git+https://github.com/ikespand/keplergl_cli
```
## Usage
There are many examples available in the example folder. Additionally, code is documented with docstrings.