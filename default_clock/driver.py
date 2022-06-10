import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 16, auto_write=False)


def push(segments):
    for i in range(16):
        pixels[i] = segments[i]

    pixels.show()


def init():
    push([(0, 0, 0)]*16)
