import display
import color_tools
import datetime


display.driver.init()


def show_clock():
    hour = datetime.datetime.now().hour
    hour_text = format(hour, 'X') if hour < 13 else format(hour-12, 'X')
    quater_colors = [(255, 42, 0), (0, 255, 42), (42, 0, 255), (140, 0, 255)]
    display.show_text(hour_text, 3, 1, 0, quater_colors[int(datetime.datetime.now().minute/15)])


show_clock()
