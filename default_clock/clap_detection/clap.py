import numpy as np
from scipy.signal import butter, lfilter
import wave
import pyaudio
import struct


lowcut = 1000
highcut = 15000
nyquist = 44100.0 / 2.0

threshold = 0.08
minblocks = 1
maxblocks = 3

max_spacing = 10

above_threshold = 0
spacing = 0
clap_count = 0

# Create filter
low = lowcut / nyquist
high = highcut / nyquist
b, a = butter(5, [low, high], btype='band')

# w = wave.open('test.wav')

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=2048, input_device_index=1)

while 1:
    # frames = w.readframes(2048)
    frames = stream.read(2048)
    samples = struct.unpack('<%dh' % 2048, frames)

    y = lfilter(b, a, samples)
    val = max(y)
    normalized = (val/32768.0)
    if normalized > threshold:
        above_threshold += 1
    else:
        spacing += 1

        if minblocks <= above_threshold <= maxblocks:
            print 'clap'
            clap_count += 1
            spacing = 0

        above_threshold = 0

        # check if spacing expired
        if spacing >= max_spacing and clap_count != 0:
            print '%d clap(s)' % clap_count
            clap_count = 0


    # outdata = struct.pack('<%dh' % 2048, *y.astype('int16'))
    # stream.write(frames)
