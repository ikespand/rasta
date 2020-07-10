# rasta

Rasta (rāstā) is a python based library specifically design to handle gpx dataset. 

## Features

-   Parse XML gps routes easily and get data in pandas df in single line of code
-   get the distance of consecutive coordinates
-   Postprocessing data for average speed, total distance
-   Integration with kepler gl allows the creation of interactive map with nice visualization

## Install

**Mapbox API key**: To use kepler gl integration, user will need to provide a Mapbox API key. Go to [Mapbox.com](https://account.mapbox.com/access-tokens)
to get an API key.

This package has dependencies on `geojson`, `shapely`, `geopandas`, `gpx` and `kepler_cli`.

```
conda install geojson shapely geopandas -c conda-forge
pip install keplergl_cli gpx kepler_cli
```

## Usage
To be documented