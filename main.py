from locations import LOCATIONS
from sources import *
from plotter import plot_forecast
import pandas as pd

location = "bilbao"        # bilbao | pradoluengo
mode = "48h"               # 48h | weekly

lat = LOCATIONS[location]["lat"]
lon = LOCATIONS[location]["lon"]

dfs = [
    openweather_forecast(lat, lon, mode),
    meteostat_forecast(lat, lon, mode),
    weatherapi_forecast(lat, lon, mode),
    tomorrow_forecast(lat, lon, mode)
]

df_all = pd.concat(dfs).sort_values("time")

plot_forecast(df_all, location, mode)
