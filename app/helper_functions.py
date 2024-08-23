import os
import datetime
from pyluach.dates import HebrewDate
from pyluach import parshios
import requests
from django.core.cache import cache


def make_weather_api_call(current_dt):
    req_url = (f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Newark,NJ/"
               f"{current_dt.strftime('%Y-%m-%d')}/"
               f"?unitGroup=us"
               f"&key={os.environ['WEATHER_API_KEY']}"
               f"&include=days"
               f"&elements=datetime,moonphase,sunrise,sunset,moonrise,moonset")

    return requests.get(req_url)


def moon_phase_mappings(phase):
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


def seconds_till_midnight(current_time):
    midnight = ((current_time + datetime.timedelta(days=1))
                .replace(hour=0, minute=0, microsecond=0, second=0))
    return (midnight - current_time).seconds


def get_moon_phase(current_dt):
    sentinel = object()
    cache_val = cache.get("moon_phase", sentinel)
    if cache_val is sentinel:
        print("CACHE MISS")
        resp = make_weather_api_call(current_dt).json()
        # Cache for at least 5s, in case we're super close to midnight
        seconds_until_midnight = max(seconds_till_midnight(current_dt), 5)
        cache.set("moon_phase", resp, timout=seconds_until_midnight)
    else:
        print("CACHE HIT")
        resp = cache.get("moon_phase")

    phase = resp['days'][0]['moonphase']
    return moon_phase_mappings(phase)


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
