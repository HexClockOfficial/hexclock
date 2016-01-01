import smbus

bus = smbus.SMBus(1)
address = 0x10


def calculate_checksum(data):
    checksum = 0
    for b in data:
        for i in range(8):
            checksum += (b >> i) & 1
    return checksum


def send_packet(segment, (r, g, b)):
    packet = [0x48, 0x45, 0x58, segment, int(r), int(g), int(b), 0]
    packet[7] = calculate_checksum(packet[3:7])
    try:
        bus.write_i2c_block_data(address, 0, packet)
        command_status = bus.read_byte(address)
        if command_status == 0xf0:
            return 1
    except IOError:
        pass
    return 0


def push(segments):
    for i in range(16):
        packet_success = 0
        while not packet_success:
            packet_success = send_packet(i, segments[i])


def init():
    push([(0, 0, 0)]*16)
