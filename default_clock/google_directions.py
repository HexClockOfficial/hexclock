import urllib
import json

key = 'AIzaSyBkbe5ZeLWXPi4-sajOau0UCi43GVz659M'
base_url = 'https://maps.googleapis.com/maps/api/directions/json?'


def get_travel_info(orig, dest):
    orig = orig.replace(' ', '+')
    dest = dest.replace(' ', '+')
    url = base_url + 'origin=%s&destination=%s&departure_time=now&traffic_model=best_guess&key=%s' % (orig, dest, key)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    travel_info = []
    for route in data['routes']:
        duration = route['legs'][0]['duration']['value']
        traffic_duration = route['legs'][0]['duration_in_traffic']['value']
        summary = route['summary']
        travel_info += [(duration, traffic_duration, summary)]
    return travel_info
