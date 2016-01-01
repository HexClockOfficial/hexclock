import threading
import time
import color_tools
import clock_ascii

try:
    import driver
except ImportError as e:
    from debug import driver_debug as driver

segments = [(0, 0, 0)]*16


def get_char_frame(char, (r, g, b)):
    frame = [(0, 0, 0)]*16
    for i in clock_ascii.char_segs(char):
        frame[i] = (r, g, b)
    return frame


def show_char(char, (r, g, b)):
    global segments
    segments = get_char_frame(char, (r, g, b))
    push_segs()


def show_text(text, delay, fade, random, (r, g, b)=(0, 0, 0)):
    for c in text:
        (r, g, b) = color_tools.random_rgb() if random else (r, g, b)
        if not fade:
            show_char(c, (r, g, b))
            time.sleep(delay)
        else:
            fade_frame(get_char_frame(c, (r, g, b)), delay*0.75)
            time.sleep(delay*0.25)


def show_frame(frame):
    global segments
    segments = list(frame)
    push_segs()


def attention():
    for loop in range(4):
        frame = [(0, 0, 0)]*16
        for color in [color_tools.random_rgb(), (0, 0, 0)]:
            for a, b in [(0, 1), (8, 9), (4, 5)]:
                frame[a] = frame[b] = color
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
