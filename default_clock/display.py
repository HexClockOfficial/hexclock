import threading
import time
import color_tools
import clock_ascii
import os

if os.name == 'nt':
    from debug import driver_debug as driver
else:
    import driver


segments = [(0, 0, 0)]*16


def get_char_frame(char, color):
    frame = [(0, 0, 0)]*16
    for i in clock_ascii.char_segs(char):
        frame[i] = color
    return frame


def show_char(char, color):
    global segments
    segments = get_char_frame(char, color)
    push_segs()


def show_text(text, delay, fade, random, color=(0, 0, 0)):
    for c in text:
        color = color_tools.random_rgb() if random else color
        if not fade:
            show_char(c, color)
            time.sleep(delay)
        else:
            fade_frame(get_char_frame(c, color), delay*0.75)
            time.sleep(delay*0.25)


def show_frame(frame):
    global segments
    segments = list(frame)
    push_segs()


def attention():
    order = [0, 1, 2, 3, 5, 4, 6, 7]

    for i in range(len(order) * 6):
        frame = [(0, 0, 0)] * 16
        for offset in range(3):
            if i - offset < 0:
                continue
            offset_color = color_tools.h_to_rgb((((i - offset) * 30.0) + 360) % 360)
            frame_index = order[(i - offset + len(order)) % len(order)]
            brightness = ((3.0 - offset) / 3.0)
            color = (offset_color[0] * brightness, offset_color[1] * brightness, offset_color[2] * brightness)
            frame[frame_index] = color

        fade_frame(frame, 0.2)


def fade_frame(frame, delay):
    global segments
    step = 1.0/20.0
    numf = int(delay/step)
    color_deltas = [((r1-r0)/numf, (g1-g0)/numf, (b1-b0)/numf) for (r1, g1, b1), (r0, g0, b0) in zip(frame, segments)]
    for f in range(numf):
        for i in range(16):
            r, g, b = segments[i]
            rd, gd, bd = color_deltas[i]
            segments[i] = (r+rd, g+gd, b+bd)
        elapsed = push_segs()
        time.sleep(max(step-elapsed, 0))
    segments = list(frame)
    push_segs()


def push_segs():
    global segments
    start = time.time()
    driver.push(segments)
    end = time.time()
    return end - start
