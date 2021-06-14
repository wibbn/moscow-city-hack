import os
import requests

def geocode(address):
    apikey = os.getenv('YNDX_GEOCODE_TOKEN')
    url = f"https://geocode-maps.yandex.ru/1.x?format=json&geocode={address}&apikey={apikey}"
    r = requests.get(url).json()

    coords = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    d = {}
    d['lng'], d['lat'] = map(float, coords.split())

    return d

def distance(x, y):
    return ((x['lat']-y['lat'])**2 + (x['lng']-y['lng'])**2)**0.5

def get_place_arround(data, x, dist):
    return data[distance(data, x) <= dist]