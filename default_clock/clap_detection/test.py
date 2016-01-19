import clap_detection


def clap_callback():
    print 'wooo'

c = clap_detection
c.init(clap_callback)
print 'init'
c.detect = True
c.detect_loop()

