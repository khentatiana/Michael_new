import socket

sock = socket.socket()

sock.bind(('', 9091))

sock.listen(1)

conn, addr = sock.accept()
name = input('Ведите ваше имя: ')
conn.send(name.encode('utf-8'))
name_2 = conn.recv(1024).decode('utf-8')


while True:
    message = input(name + ': ')

    if message == 'end':
        conn.send('end'.encode('utf-8'))
        sock.close()

    conn.send(message.encode('utf-8'))

    client_data = conn.recv(1024)
    client_string = client_data.decode('utf-8')
    print(name_2 + ': ' + client_string)

    if client_string == 'end':
        sock.close()
