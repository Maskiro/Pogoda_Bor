import json
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib import request
def get_weather():
    with request.urlopen('https://api.open-meteo.com/v1/forecast?latitude=56.3594&longitude=44.073&hourly=temperature_2m,precipitation&timezone=Europe%2FMoscow') as response:
        ht = response.read().decode('utf-8')
    dic = json.loads(ht)
    return dic
def get_temp(weather):
    time = datetime.now(ZoneInfo("Europe/Moscow")).strftime('%Y-%m-%dT%H:00')
    index = weather['hourly']['time'].index(time)
    temperature = weather['hourly']['temperature_2m'][index]
    precipitation = weather['hourly']['precipitation'][index]
    current_time = weather['hourly']['time'][index]
    return temperature, precipitation, current_time