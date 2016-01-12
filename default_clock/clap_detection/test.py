import clap_detection


def clap_callback():
    print 'wooo'


c = clap_detection
c.init(clap_callback)
print 'init'
c.start_detection()
print 'detecting'

while True:
    yes = 0
