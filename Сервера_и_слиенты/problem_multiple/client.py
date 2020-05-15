from Сервера_и_слиенты.problem_multiple.go_to_network import *
import threading


def receive_broadcast(server):
    while True:
        message = receive_string(server)

        if message:
            if message[-5:] == '!file':
                receive_file(server)
            else:
                print(message)


name = input('Введите ваше имя: ')
client = Client('127.0.0.1', 9090, name)
connection = client.connection

threading.Thread(target=receive_broadcast, args=[connection])

while True:
    message = input()
    if message == '!bye':
        send_string(connection, message)
        break
    if message == '!file':
        send_string(connection, message)
        filename = input('Введите имя фаила: ')

        send_file(connection, filename)
    if message == '!message':
        print('Имя user который вы бы хотели послать личное сообшение: ')
        person = input()
        print('Сообшение: ')
        message = input()

        send_string(connection, person)
        send_string(connection, message)

connection.close()
