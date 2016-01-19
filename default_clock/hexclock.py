## -*- coding: UTF-8 -*-

import display
import color_tools
import clap_detection
import google_directions
import tcp_passthrough

import datetime
import time
import pywapi

display_override = False


def show_clock():
    hour = datetime.datetime.now().hour
    hour_text = format(hour, 'X') if hour < 13 else format(hour-12, 'X')
    hour_color = color_tools.h_to_rgb((datetime.datetime.now().minute/15)*90)
    display.show_text(hour_text, 3, 1, 0, hour_color)


def clap_callback():
    global display_override
    display_override = True

    original = display.segments[:]
    bright = [(255, 255, 255) if r != 0 or g != 0 or b != 0 else (0, 0, 0) for r, g, b in original]
    display.fade_frame(bright, 0.2)
    display.fade_frame(original, 0.2)

    display_override = False


def detection_callback(claps):
    global display_override
    display_override = True

    if claps == 2:
        show_weather()

    if claps == 3:
        home = '609 Cornell Dr 78660'
        work = '828 New Meister Lane 78660'
        cathy = '4009 Victory Dr 78704'

        show_route(home, cathy)

    show_clock()
    display_override = False


def show_weather():
    yahoo_weather = pywapi.get_weather_from_yahoo('78660', 'imperial')
    weather_text = yahoo_weather['condition']['text']
    temperature_normalized = min(max(int(yahoo_weather['condition']['temp'])-30, 0), 90)/60.0
    temperature_color = (int(0+(255.0*temperature_normalized)), 0, int(255-(255.0*temperature_normalized)))
    temperature_text = u'%s\xb0F' % yahoo_weather['condition']['temp']

    display.show_text(temperature_text, 0.5, 0, 0, temperature_color, 0.1)
    time.sleep(1)
    display.show_text(weather_text, 0.3, 0, 0, (150, 150, 150), 0.1)


def show_route(origin, destination):
    routes = google_directions.get_travel_info(origin, destination)
    for route in routes:
        in_traffic_time = abs(route.traffic_duration-route.duration)
        in_traffic_normalized = min(in_traffic_time, 480)/480.0
        traffic_color = (int(0+(255.0*in_traffic_normalized)), int(255-(255.0*in_traffic_normalized)), 0)
        route_time_text = '%dM %dT' % (route.traffic_duration/60, in_traffic_time/60)

        display.show_text(route_time_text, 0.5, 0, 0, traffic_color, 0.1)
        time.sleep(1)
        display.show_text(route.summary, 0.3, 0, 0, traffic_color, 0.1)


clap = clap_detection.ClapDetect(detection_callback, clap_callback)
clap.start_detection()

tcp = tcp_passthrough
tcp.init()

while 1:
    if not display_override and not tcp.connected:
        show_clock()
    time.sleep(30)

