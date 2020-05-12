import socket


sock = socket.socket()

sock.connect(('192.168.1.92', 9091))

server_name = sock.recv(1024).decode('utf-8')

name = input('Ведите ваше имя: ')
sock.send(name.encode('utf-8'))

while True:
    server_data = sock.recv(1024)
    server_string = server_data.decode('utf-8')

    print(server_name + ': ' + server_string)

    if server_string == 'end':
        sock.close()

    message = input(name + ': ')

    if message == 'end':
        sock.send('end'.encode('utf-8'))
        sock.close()

    sock.send(message.encode('utf-8'))
