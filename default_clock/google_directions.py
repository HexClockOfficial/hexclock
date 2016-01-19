import urllib
import json

key = 'AIzaSyBkbe5ZeLWXPi4-sajOau0UCi43GVz659M'
base_url = 'https://maps.googleapis.com/maps/api/directions/json?'


class Route:
    duration = ''
    traffic_duration = ''
    summary = ''

    def __init__(self, duration, traffic_duration, summary):
        self.duration = duration
        self.traffic_duration = traffic_duration
        self.summary = summary


def get_travel_info(origin, destination):
    origin = origin.replace(' ', '+')
    destination = destination.replace(' ', '+')
    url = base_url + 'origin=%s&' \
                     'destination=%s&' \
                     'departure_time=now&traffic_model=best_guess&key=%s' % (origin, destination, key)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    travel_info = []
    for route in data['routes']:
        duration = route['legs'][0]['duration']['value']
        traffic_duration = route['legs'][0]['duration_in_traffic']['value']
        summary = route['summary']
        travel_info += [Route(duration, traffic_duration, summary)]
    return travel_info

home = '609 Cornell Dr 78660'
work = '828 New Meister Lane 78660'
cathys = '4009 Victory Dr 78704'
routes = get_travel_info(home, cathys)
