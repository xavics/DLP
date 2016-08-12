import json
import os

import requests
from os.path import dirname, join, abspath
from os import system
import datetime
import time

from DLP.settings import WEATHER_API_KEY, STATIC_ROOT
from dlp.models import City

TEMPLATE_PATH = abspath(join(dirname(__file__), "templates/temperature.html"))
GENERATED_PATH = abspath(join(dirname(__file__), "generated"))


def get_weather_by_geo(lat, lng):
    params = {'lat': lat, 'lon': lng, 'units': "metric",
              'APPID': WEATHER_API_KEY}
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather'
        response = requests.get(url=url, params=params)
        return response.text
    except KeyError:
        pass


def generate_weather_image(city):
    city = City.objects.get(id=city)
    json_data = get_weather_by_geo(city.lat, city.lng)
    data = json_loads_byteified(json_data)
    print data
    html_path = generate_html(
        city.name, data['weather'][0]['description'],
        data['weather'][0]['icon'], data['coord']['lat'],
        data['coord']['lon'], data['main']['temp'],
        data['main']['temp_max'], data['main']['temp_min'],
        data['wind']['speed'], data['clouds']['all'],
        data['main']['pressure'], data['main']['humidity']
    )
    image_path = generate_image(html_path)
    return image_path


def generate_html(name, description, id_icon, lat, lon, temp, temp_max,
                  temp_min, wind, cloud, pressure, humidity):
    base = open(TEMPLATE_PATH, "r")
    print "reading"
    string_file = base.read()
    generated_html = string_file.format(
        city=name, icon=str(id_icon), desc=description.title(), lat=str(lat),
        lon=str(lon), temp=str(temp), temp_max=str(temp_max),
        temp_min=str(temp_min), cloud=str(cloud), wind=str(wind),
        pressure=str(pressure), humidity=str(humidity)
    )
    base.close()
    html_path = join(GENERATED_PATH, "temperature.html")
    temp = open(html_path, "w")
    temp.write(generated_html)
    temp.close()
    return html_path


def generate_image(html_path):
    image_name = "images/temperature_{time}.png".format(
        time=int(time.mktime(datetime.datetime.now().timetuple())))
    image_path = join(STATIC_ROOT, image_name)
    remove_update_temp(join(STATIC_ROOT, "images"))
    system(
        "cutycapt --url=file:{html} --out={image} --min-width=600 " \
        "--min-height=250".format(html=html_path, image=image_path))
    return join("static", image_name)


def can_fly(lat, lng):
    json_data = get_weather_by_geo(lat, lng)
    data = json_loads_byteified(json_data)
    available = True
    if "wind" in data:
        if "speed" in data["wind"]:
            if data['wind']['speed'] >= 10.0:
                available = False
    if "rain" in data:
        available = False
    return available


def remove_update_temp(image_path):
    print image_path
    os.system("find {path} -type f -name '*{name}*' -delete".format(
        path=image_path, name="temperature"))


# Extracted from

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True):
                _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
            }
    # if it's anything else, return it in its original form
    return data
