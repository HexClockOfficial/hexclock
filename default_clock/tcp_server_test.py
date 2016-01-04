import display
import color_tools
import tcp_passthrough

import time
import datetime
import socket


def show_clock():
    hour = datetime.datetime.now().hour
    hour_text = format(hour, 'X') if hour < 13 else format(hour-12, 'X')
    hour_color = color_tools.h_to_rgb((datetime.datetime.now().minute/15)*90)
    display.show_text(hour_text, 3, 1, 0, hour_color)

display.driver.init()
tcp_passthrough.init()

while True:
    if not tcp_passthrough.connected:
        show_clock()
        time.sleep(30)

