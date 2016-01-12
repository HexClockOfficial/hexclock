import alsaaudio

card = 'sysdefault:CARD=Device'
f = open('out.wav', 'wb')
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
inp.setchannels(1)
inp.setrate(44100)
inp.setperiodsize(2048)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

length, data = inp.read()
print length
print len(data)
print '--------------------------------'
print data

# i=250
# while i > 0:
#   length,data = inp.read()
#   f.write(data)
#   i-=1