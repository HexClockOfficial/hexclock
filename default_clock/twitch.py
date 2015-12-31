import socket
from urllib import urlopen
import json


def channel_streaming(user):
    url = 'https://api.twitch.tv/kraken/streams/' + user
    try:
        info = json.loads(urlopen(url).read().decode('utf-8'))
        if info['stream'] is not None:
            return 1
    except:
        pass
    return 0
