import os
import datetime
from pyluach.dates import HebrewDate
from pyluach import parshios
import requests


def get_moon_phase(current_dt):
    req_url = (f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Newark,NJ/"
               f"{current_dt.strftime('%Y-%m-%d')}"
               f"?unitGroup=us"
               f"&key={os.environ['WEATHER_API_KEY']}"
               f"&include=days"
               f"&elements=datetime,moonphase,sunrise,sunset,moonrise,moonset")

    resp = requests.get(req_url)
    phase = resp.json()['days'][0]['moonphase']

    if phase == 0:
        return "New_Moon"
    elif 0.0 < phase < 0.25:
        return "Waxing_Crescent"
    elif phase == 0.25:
        return "First_Quarter"
    elif 0.25 < phase < 0.5:
        return "Waxing_Gibbous"
    elif phase == 0.5:
        return "Full_Moon"
    elif 0.5 < phase < 0.75:
        return "Waning_Gibbous"
    elif phase == 0.75:
        return "Last_Quarter"
    elif 0.75 < phase <= 1.0:
        return "Waning_Crescent"
    else:
        return "Unknown"


def get_date_time_ctx():
    dt = datetime.datetime.now()
    moon_phase = get_moon_phase(dt)
    hebrew_dt = HebrewDate.from_pydate(dt)
    parsha = parshios.getparsha_string(hebrew_dt)
    ctx = {
        'dt': dt,
        'moon_phase': moon_phase,
        'hebrew_dt': hebrew_dt,
        'parsha': parsha,
        'ivrit_day': hebrew_dt.hebrew_date_string()
    }
    return ctx
