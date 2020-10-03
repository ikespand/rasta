# rasta

Rasta (rāstā) is a Python based library specifically design to handle gpx dataset. 

## Features

-   Parse XML gps routes easily and get data in pandas df in a single line of code
-   Get the distance of consecutive coordinates and perform calculation of speed (if timestamp is available)
-   Postprocessing data for average speed, total distance
-   Integration with kepler gl allows the creation of interactive map with nice visualization

## Install

**Mapbox API key**: To use kepler gl integration, user will need to provide a Mapbox API key. Go to [Mapbox.com](https://account.mapbox.com/access-tokens)
to get an API key.

This package has dependencies on `geojson`, `shapely`, `geopandas`, `gpx` and `kepler_cli`. For `kepler_cli`

```
conda install geojson shapely geopandas -c conda-forge
pip install gpx 
pip install git+https://github.com/ikespand/keplergl_cli
```

## Usage
To be documented