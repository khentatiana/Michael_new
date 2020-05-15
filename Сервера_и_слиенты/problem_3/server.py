import socket
from Сервера_и_слиенты.problem_3.go_to_network import *

sock = socket.socket()

sock.bind(('', 9090))

sock.listen(1)

print('Server listening....')

while True:
    conn, addr = sock.accept()
    name = receive_string(conn)
    print('Got connection from', addr)

    while True:
        file_name = receive_string(conn)
        if file_name == 'end':
            break

        file = receive_data(conn).decode('utf-8')

        if file_name:
            print('Фаил получен от ' + name + '.')

            new_file = open('new_' + file_name, 'w')
            new_file.write(file)
            new_file.close()

    print('Disconnected', addr)
    conn.close()
