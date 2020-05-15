import struct


def send_data(sock, data):
    size = len(data)
    size_bytes = struct.pack(">I", size)
    sock.send(size_bytes)
    sock.send(data)


def receive_data(sock):
    size_bytes = sock.recv(4)
    size = struct.unpack('>I', size_bytes)[0]
    data = sock.recv(size)

    return data


def send_string(sock, s):
    send_data(sock, s.encode('utf-8'))


def receive_string(sock):
    return receive_data(sock).decode('utf-8')
