import socket

# создаем сокет
sock = socket.socket()
# подключаемся к 127.0.0.1:9090
sock.connect(('127.0.0.1', 9090))

s = input()

# отправляем данные, предварительно закодировав в utf-8
sock.send(s.encode('utf-8'))
print('Отправили...')

# ждем, пока не придет ответ, а когда он пришел, читаем из буфера все данные, но не более 1024 байт
result_data = sock.recv(1024)
print('Получили...')

# нужно превратить байты в строку - декодируем utf-8
result_string = result_data.decode('utf-8')

# выводим на экран
print(result_string)

# закрываем соединение
sock.close()
