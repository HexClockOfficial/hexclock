import requests
import json
# API key
api_key = '2c68c778cdc88feb793e6e2b6a3310e4'

# Pflugerville lat lon
pville_lat = 30.446111
pville_lon = -97.623889


def get_current_temp():
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s&units=imperial' % (pville_lat, pville_lon, api_key)
        result = requests.get(url)
        result_json = json.loads(result.content)

        return True, result_json['main']['temp']
    except:
        return False, 0
