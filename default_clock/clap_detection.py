from scipy.signal import butter, lfilter
import pyaudio
import struct
import threading


class ClapDetect:
    filter_a, filter_b = 0, 0
    stream = 0

    detect_callback = 0
    clap_callback = 0

    threshold = 0.04
    min_blocks = 1
    max_blocks = 3

    max_spacing = 10

    detect = False

    def __init__(self, detect_callback, clap_callback, low_cutoff=1000, high_cutoff=15000, device_index=2, rate=44100):
        self.detect_callback = detect_callback
        self.clap_callback = clap_callback
        self.filter_b, self.filter_a = butter(5, [low_cutoff/(rate/2.0), high_cutoff/(rate/2.0)], btype='band')
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, input_device_index=device_index)

    def start_detection(self):
        self.detect = True
        t = threading.Thread(target=self.detect_loop)
        t.daemon = True
        t.start()

    def detect_loop(self):
        above_threshold = 0
        spacing = 0
        clap_count = 0

        frame_buffer = ''

        while self.detect:
            try:
                frame_buffer += self.stream.read(1024)
                if len(frame_buffer) >= (2048*2):
                    samples = struct.unpack('<%dh' % 2048, frame_buffer)
                    frame_buffer = ''

                    filtered = lfilter(self.filter_b, self.filter_a, samples)
                    block_max = max(filtered)
                    normalized = (block_max/32768.0)
                    if normalized > self.threshold:
                        above_threshold += 1
                    else:
                        spacing += 1

                        if self.min_blocks <= above_threshold <= self.max_blocks:
                            t = threading.Thread(target=self.clap_callback)
                            t.daemon = True
                            t.start()
                            clap_count += 1
                            spacing = 0

                        if spacing >= self.max_spacing and clap_count != 0:
                            t = threading.Thread(target=self.detect_callback, args=[clap_count])
                            t.daemon = True
                            t.start()
                            clap_count = 0

                        above_threshold = 0
            except IOError:
                pass
