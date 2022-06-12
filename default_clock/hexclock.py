import display
import datetime
import time
import weather

display.driver.init()


def show_clock():
    hour = datetime.datetime.now().hour
    hour_text = format(hour, 'X') if hour < 13 else format(hour-12, 'X')
    quarter_colors = [(255, 42, 0), (0, 255, 42), (20, 0, 255), (140, 0, 255)]
    display.show_text(hour_text, 3, 1, 0, quarter_colors[int(datetime.datetime.now().minute/15)])


while True:
    if datetime.datetime.now().minute % 5 == 0:
        success, temp_now = weather.get_current_temp()
        if success:
            display.attention()
            display.show_text('TEMP ', 1, False, True)
            display.show_text('%d' % temp_now, 1.5, False, True)

    show_clock()

    time.sleep(60)
