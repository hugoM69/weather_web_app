import streamlit as st
import pandas as pd

from locations import LOCATIONS
from sources import (
    openweather_forecast,
    meteostat_forecast,
    weatherapi_forecast,
    tomorrow_forecast
)
from plotter import plot_forecast
st.set_page_config(page_title="Comparador Meteo", layout="wide")

st.title("🌦️ Comparador de previsiones meteorológicas")

location = st.selectbox(
    "📍 Selecciona ubicación",
    ["bilbao", "pradoluengo"]
)

mode = st.radio(
    "⏱️ Tipo de previsión",
    ["48h", "weekly"],
    horizontal=True
)

if st.button("🔍 Obtener previsión"):
    lat = LOCATIONS[location]["lat"]
    lon = LOCATIONS[location]["lon"]

    with st.spinner("Descargando datos..."):
        dfs = [
            openweather_forecast(lat, lon, mode),
            meteostat_forecast(lat, lon, mode),
            weatherapi_forecast(lat, lon, mode),
            tomorrow_forecast(lat, lon, mode)
        ]

    df_all = pd.concat(dfs).sort_values("time")

    st.success("Previsión cargada")

    st.pyplot(plot_forecast(df_all, location, mode))
