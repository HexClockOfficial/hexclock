import clap_detection_wav


def clap_callback():
    print 'wooo'


c = clap_detection_wav
c.init(clap_callback)
print 'init'
c.start_detection()
print 'detecting'

while True:
    yes = 0
