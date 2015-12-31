import datetime
from astral import Astral

on = (200, 200, 200)
off = (0, 0, 83)

new_moon_icon = [off]*16
first_quarter_icon = [off, on, on, on, off, on, off, off, off, on, off, on, on, on, on, off]
full_moon_icon = [on]*16
last_quarter_icon = [on, off, off, off, on, off, on, on, on, off, on, on, off, off, on, on]


def get_phase_segment():
    a = Astral()
    moon_phase = a.moon_phase(datetime.datetime.now())
    if 0 < moon_phase < 4:
        return new_moon_icon
    if 4 < moon_phase < 10:
        return first_quarter_icon
    if 10 < moon_phase < 17:
        return full_moon_icon
    if 17 < moon_phase < 26:
        return last_quarter_icon
    if 26 < moon_phase < 29:
        return new_moon_icon
