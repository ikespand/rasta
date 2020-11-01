"""
Rasta has a module to postprocess data for navigation coming from the REST API
of OpenTrip Planner (https://ikespand.github.io/posts/OpenTripPlanner/).

Just for reference:
# APIKEY= "Bearer a559433c8d2d91b2329f24457b6dc122"
# address = "https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals?lat=48.780816&lon=9.201172&radius=2000&limit=4&providernetwork=2"
# response = requests.get(address, headers={"Authorization":APIKEY})
# http://localhost:8080/otp/routers/default/plan?fromPlace=28.69782,77.19269&toPlace=28.60743,77.22702
# http://localhost:8080/otp/routers/default/isochrone?&fromPlace=28.60743,77.22702&date=2015/01/09&time=12:00:00&mode=WALK&&walkSpeed=5&cutoffSec=1800&cutoffSec=3600
# aa=response.json()
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
pts.to_csv("it1.csv", index=False)
