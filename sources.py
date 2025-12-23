import requests
import pandas as pd
from meteostat import Hourly, Daily
from datetime import datetime, timedelta


OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
AEMET_KEY = eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJsb2xlcm9sb2xldGVAZ21haWwuY29tIiwianRpIjoiZDU5MDljNmEtOWU0ZC00YjkyLWEzMTEtMDc1NTc1YTU0YTgzIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NjY1MDkwNDIsInVzZXJJZCI6ImQ1OTA5YzZhLTllNGQtNGI5Mi1hMzExLTA3NTU3NWE1NGE4MyIsInJvbGUiOiIifQ.w_EPwdIpwWC7s104aJg4MrdCleOHSpqpu2gOQLKwfmQ
TOMORROW_API_KEY = st.secrets["TOMORROW_API_KEY"]

def openweather_forecast(lat, lon, mode):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    data = requests.get(url, params=params).json()["list"]

    df = pd.DataFrame([{
        "time": pd.to_datetime(d["dt"], unit="s"),
        "temp": d["main"]["temp"]
    } for d in data])

    if mode == "weekly":
        df = df.resample("D", on="time").mean().reset_index()

    df["source"] = "OpenWeather"
    return df

def meteostat_forecast(lat, lon, mode):
    now = datetime.utcnow()

    if mode == "48h":
        data = Hourly(lat, lon, now, now + timedelta(hours=48)).fetch()
    else:
        data = Daily(lat, lon, now, now + timedelta(days=7)).fetch()

    df = data.reset_index()[["time", "temp"]]
    df["source"] = "Meteostat"
    return df

def weatherapi_forecast(lat, lon, mode):
    days = 7 if mode == "weekly" else 2
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": f"{lat},{lon}",
        "days": days,
        "aqi": "no",
        "alerts": "no"
    }
    data = requests.get(url, params=params).json()["forecast"]["forecastday"]

    rows = []
    for d in data:
        if mode == "48h":
            for h in d["hour"]:
                rows.append({
                    "time": pd.to_datetime(h["time"]),
                    "temp": h["temp_c"]
                })
        else:
            rows.append({
                "time": pd.to_datetime(d["date"]),
                "temp": d["day"]["avgtemp_c"]
            })

    df = pd.DataFrame(rows)
    df["source"] = "WeatherAPI"
    return df

def tomorrow_forecast(lat, lon, mode):
    timesteps = "1h" if mode == "48h" else "1d"
    url = "https://api.tomorrow.io/v4/timelines"
    params = {
        "apikey": TOMORROW_API_KEY
    }
    payload = {
        "location": f"{lat},{lon}",
        "fields": ["temperature"],
        "timesteps": [timesteps],
        "units": "metric"
    }

    data = requests.post(url, params=params, json=payload).json()
    intervals = data["data"]["timelines"][0]["intervals"]

    df = pd.DataFrame([{
        "time": pd.to_datetime(i["startTime"]),
        "temp": i["values"]["temperature"]
    } for i in intervals])

    df["source"] = "Tomorrow.io"
    return df

