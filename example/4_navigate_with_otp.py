#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rasta has a module to postprocess data for navigation coming from the REST API
of OpenTrip Planner (https://ikespand.github.io/posts/OpenTripPlanner/).
"""
# %%

from settings import MAPBOX_API_KEY
from navigate_with_otp import GetOtpRoute
import pandas as pd
import numpy as np

# %%
my_otp_nav = GetOtpRoute(
    start_coord="28.658420, 77.230757",
    end_coord="28.544442, 77.206334",
    MAPBOX_API_KEY=MAPBOX_API_KEY,
    output_map_path="temporary_map_",
    viz=False,
)
my_otp_nav.address
gdf, html_path = my_otp_nav.extract_itinerary()

# %%

# To extract and postporcess
ite1 = gdf[0]
ite1 = ite1.reset_index(drop=True)
bus = ite1.loc[[1]]


pt = np.array(bus.geometry.values[0].coords)
time = 40

pts = pd.DataFrame(columns=["latitude", "longitude", "time"])
pts["latitude"] = pt[:, 1]
pts["longitude"] = pt[:, 0]
pts["time"] = time / 18
pts["time"] = pts["time"].cumsum()
#pts.to_csv("it1.csv", index=False)
