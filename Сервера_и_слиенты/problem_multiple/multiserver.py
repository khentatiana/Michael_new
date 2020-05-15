from Сервера_и_слиенты.problem_multiple.go_to_network import *
import threading
import json


connections = []


def send_broadcast(message, connection):
    if message == '!message':
        person = receive_string(connection)
        found = False
        for c in connections:
            if c.name == person:
                new_message = receive_string(connection)
                send_string(c, connection.name + '(личьное): ' + new_message)
                found = True
                break

        if not found:
            send_string(connection, 'Сервер: Нету человека с токим ником в чате.')
    else:
        for c in connections:
            if c.name != connection.name:
                if message == '!file':
                    send_string(c, connection.name + ': ' + message)
                    file_name = receive_string(connection)
                    send_file(c, file_name)

                if message == '!bye':
                    send_string(c, connection.name + ' отключился.')


def receive_message(connection):
    while True:
        message = receive_string(connection)
        if message:
            send_broadcast(message, connection)


server = Server(9090)

while True:
    connections.append(server.accept())
    threading.Thread(target=receive_message, args=[connections[-1]])
