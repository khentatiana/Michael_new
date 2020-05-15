import struct
import socket


class Connection:
    def __init__(self, conn, name, addr=None):
        self.connection = conn
        self.addr = addr
        self.name = name

    def send(self, data):
        if self.connection:
            if type(data) == str:
                send_string(self.connection, data)
            else:
                send_data(self.connection, data)

    def receive_string(self):
        if self.connection:
            return receive_string(self.connection)

    def receive_data(self):
        if self.connection:
            return receive_data(self.connection)

    def close(self):
        if self.connection:
            self.connection.close()


class Server:
    def __init__(self, port, host=''):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(10)
        self.addr = None

    def accept(self):
        connection, addr = self.socket.accept()
        name = receive_string(connection)
        return Connection(connection, name, addr)


class Client:
    def __init__(self, host, port, name):
        connection = socket.socket()
        connection.connect((host, port))
        self.connection = Connection(connection, name)


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


def send_file(sock, filename):
    try:
        with open("file_folders/" + filename, "rb") as file:
            data = file.read()
            send_string(sock, filename)
            send_data(sock, data)
            print("Фаил отправлен!")
    except FileNotFoundError:
        print("Фаил не найден.")
    except:
        print("Ошибка со стороона сервера.")


def receive_file(sock):
    file_name = receive_string(sock)
    file = receive_data(sock).decode('utf-8')

    print('Фаил получен от ' + sock.name + '.')

    y_n = '#'
    while y_n.lower() not in ['д', 'н', 'да', 'нет']:
        print('Хотите ли вы принять ' + file_name + ' от ' + sock.name + '? ', end='')
        y_n = input()

    if y_n.lower() in ['д', 'да']:
        new_file = open('new_' + file_name, 'w')
        new_file.write(file)
        new_file.close()


def send_string(sock, s):
    send_data(sock, s.encode('utf-8'))


def receive_string(sock):
    return receive_data(sock).decode('utf-8')
