from Сервера_и_слиенты.problem_multiple.go_to_network import *
import threading
import time
import json


name = input('Ведите ваше имя: ')
client = Client('176.119.157.148', 9090, name)

connection = client.connection
connection.send(name)
print("connected")


def receive_broadcast(self):
    try:
        while True:
            m = self.receive_string()
            if m:
                if m[-5:] == 'фаил.':
                    new_file = open('received_file', 'w')
                    file_sent = receive_data(connection)
                    for l in file_sent:
                        new_file.write(l.decode('utf-8'))
                print(m)
            time.sleep(0.1)
    except:
        pass


while True:
    thread = threading.Thread(target=receive_broadcast, args=[connection]).start()

    message = input('Вы: ')
    if message == '!help':
        print('    1) !bye -> отключиться от чата.')
        print('    2) !message -> написать кому-то в личные сообшение')
        print('    3) !file -> послать фаил всем в чате.')
        print('    4) !help -> показывает все команды.')

    elif message == '!bye':
        send_data(connection, '!bye')
        break

    elif message == '!file':
        file_name, file_type = input('Ведите имя фаила и раширения фаила: ').split('.' or ',' or ' ')
        my_file = file_name + '.' + file_type
        try:
            with open(my_file, "rb") as file:
                data = file.read()
                send_string(connection, '!file: ' + my_file)
                send_data(connection, data)
        except FileNotFoundError:
            print("File not found")
        except:
            print("Network error")

    else:
        send_string(connection, message)

connection.close()
print("end")
