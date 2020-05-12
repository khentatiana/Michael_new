from go_to_network import *
import threading
import json


server = Server(9090)


def broadcast_message(client, message):
    for c in clients:
        if c.name != client.name:
            c.send(message)


def process_client(connection):
    while True:
        message = connection.receive_string()

        if message == "!bye":
            message = 'отключился!'
            print(f'{connection.name} {message}')
            message = connection.name + ' ' + message
            broadcast_message(connection, message)
            clients.pop(clients.index(connection))
            break

        if message[:5] == "!file":
            new_file = open('received_' + message[7:], 'w')
            file_sent = receive_data(connection)
            for l in file_sent:
                new_file.write(l.decode('utf-8'))
            print(connection.name + 'Отправил всем фаил.')
            broadcast_message(connection, connection.name + 'Отправил всем фаил.')
            for c in clients:
                if c.name != connection.name:
                    send_data(c, file_sent)

        elif message:
            print(f'{connection.name}: {message}')
            broadcast_message(connection, f'{connection.name}: {message}')
    connection.close()


global clients
clients = []


while True:
    connect = server.accept()
    print(connect.name + ' подключился!')
    clients.append(connect)
    threading.Thread(target=process_client, args=[connect]).start()
