import socket
from Сервера_и_слиенты.problem_3.go_to_network import *

sock = socket.socket()
sock.connect(('127.0.0.1', 9090))
send_string(sock, input('Введите ваше имя: '))

while True:
    filename = input("Введите имя фаила: ")
    if filename == 'end':
        send_string(sock, 'end')
        break
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

sock.close()
