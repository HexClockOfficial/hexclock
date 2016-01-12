from scipy.signal import butter, lfilter
import alsaaudio
import struct
import threading

filter_a, filter_b = 0, 0
stream = 0
detection_callback = 0

threshold = 0.05
min_blocks = 1
max_blocks = 6

max_spacing = 20

detect = False


def init(callback, low_cutoff=1000, high_cutoff=15000, card='sysdefault:CARD=Device'):
    global filter_a, filter_b, stream, detection_callback
    detection_callback = callback
    filter_b, filter_a = butter(5, [low_cutoff/22050.0, high_cutoff/22050.0], btype='band')
    stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    stream.setchannels(1)
    stream.setrate(44100)
    stream.setperiodsize(2048)
    stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)


def start_detection():
    global detect
    detect = True
    t = threading.Thread(target=detect_loop)
    t.start()


def detect_loop():
    global detect, filter_a, filter_b, stream, threshold, min_blocks, max_blocks, max_spacing

    above_threshold = 0
    spacing = 0
    clap_count = 0

    while detect:
        try:
            length, frames = stream.read()
            samples = struct.unpack('<%dh' % length, frames)

            filtered = lfilter(filter_b, filter_a, samples)
            block_max = max(filtered)
            normalized = (block_max/32768.0)
            if normalized > threshold:
                above_threshold += 1
            else:
                spacing += 1

                if min_blocks <= above_threshold <= max_blocks:
                    print 'clap'
                    clap_count += 1
                    spacing = 0

                above_threshold = 0

                if spacing >= max_spacing and clap_count != 0:
                    print '%d clap(s)' % clap_count
                    clap_count = 0
        except:
            pass
