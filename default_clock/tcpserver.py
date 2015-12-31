import socket
import threading

main_socket = None
connected = False
server_up = True


# def decode_data(data):
#     for i in range(8):
#         display.segments[i] = [ord(data[(i*3)]), ord(data[(i*3)+1]), ord(data[(i*3)+2])]
#     display.push_segs()


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
            # decode_data(data)
            placeholder = 0
        else:
            conn.close()
            connected = False


def threaded_loop():
    global main_socket, connected, server_up
    while server_up:
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
