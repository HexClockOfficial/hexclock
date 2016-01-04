import socket
import threading
import display

main_socket = None
connected = False
accepting_conns = 1


def decode_data(data):
    data_start = data.index('HEX') + 3
    if (len(data)-data_start) >= 48:
        frame = [(0, 0, 0)]*16
        for i in range(16):
            frame[i] = ord(data[(i*3)+0+data_start]), ord(data[(i*3)+1+data_start]), ord(data[(i*3)+2+data_start])
        display.show_frame(frame)


def receive(conn):
    global connected
    while connected:
        data = ''
        try:
            data = conn.recv(512)
        except:
            conn.close()
            connected = False

        if data != '':
            decode_data(data)
        else:
            conn.close()
            connected = False


def threaded_loop():
    global main_socket, connected, accepting_conns
    while accepting_conns:
        conn, addr = main_socket.accept()
        connected = True
        receive(conn)


def init(connection=('', 46692)):
    global main_socket
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.bind(connection)
    main_socket.listen(1)

    loop = threading.Thread(target=threaded_loop)
    loop.daemon = True
    loop.start()
