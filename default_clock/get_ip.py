import socket
import struct

debugging = 0

try:
    import fcntl
except ImportError:
    debugging = 1


def get_ip_address(ifname):
    if debugging:
        return socket.gethostbyname(socket.gethostname())
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
