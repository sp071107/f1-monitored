import fastf1
import pandas as pd
from pathlib import Path


def enable_cache():
    cach_dir = Path("cache")
    cach_dir.mkdir(exist_ok=True)
    fastf1.Cache.enable_cache(str(cach_dir))


def build_weather_data(year,event,session_type):

    session = fastf1.get_session(year, event, session_type)
    session.load()

    weather_df = session.weather_data.copy()

    weather_cols = {
        "Time": "time",
        "AirTemp": "air_temp",
        "TrackTemp": "track_temp",
        "Humidity": "humidity",
        "Pressure": "pressure",
        "WindSpeed": "wind_speed",
        "WindDirection": "wind_direction",
        "Rainfall": "rainfall"
    }

    weather_df = weather_df.rename(columns=weather_cols)
    #print(weather_df.dtypes)
    weather_df["rainfall"] = weather_df["rainfall"].astype(int)
    weather_df["time"] = weather_df["time"].dt.total_seconds()
    #print(weather_df.dtypes)

    #print(weather_df["rainfall"].value_counts())
    #print(weather_df["rainfall"])
    #print(weather_df["time"])
    print(weather_df.isna().sum()) #for start we want to map and count the NaN values in our dataframe...WE WILL HANDLE THE NaN VALUES LATER!!!

    weather_df.to_csv("weather_data.csv", index=False)
    #print (weather_df)
    return weather_df

   
if __name__ == "__main__":
    enable_cache()
    build_weather_data(2024,"Silverstone","R")


