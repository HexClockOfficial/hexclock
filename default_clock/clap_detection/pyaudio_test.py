import pyaudio
import wave

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i, dev['name'], dev['maxInputChannels'], dev['defaultSampleRate']))


stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input_device_index=2, input=True)

wf = wave.open('outputtest.wav', 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)

for i in range(100):
    try:
        wf.writeframes(stream.read(2048))
    except IOError:
        pass
wf.close()
