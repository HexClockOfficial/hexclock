import numpy as np
from scipy.signal import butter, lfilter
import wave
import pyaudio
import struct


lowcut = 1000
highcut = 15000
nyquist = 44100.0 / 2.0

# Create filter
low = lowcut / nyquist
high = highcut / nyquist
b, a = butter(5, [low, high], btype='band')

w = wave.open('test.wav')

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(w.getsampwidth()), channels=w.getnchannels(), rate=w.getframerate(), output=True)

while 1:
    frames = w.readframes(512)
    samples = struct.unpack('<%dh' % 512, frames)

    y = lfilter(b, a, samples)
    outdata = struct.pack('<%dh' % 512, *y.astype('int16'))
    stream.write(outdata)
