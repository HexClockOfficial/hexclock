import pyaudio
import struct

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=2)

frame_buffer = ''

while True:
    try:
        frame_buffer += stream.read(1024)
        if len(frame_buffer) >= (2048*2):
            samples = struct.unpack('<%dh' % 2048, frame_buffer)
            frame_buffer = ''

            print max(samples)
    except IOError:
        # print 'rr'
        pass
