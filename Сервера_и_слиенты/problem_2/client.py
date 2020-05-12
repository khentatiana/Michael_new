import socket


sock = socket.socket()

sock.connect(('127.0.0.1', 9090))
s = input('Ведите ваще число: ')

sock.send(s.encode('utf-8'))

result = sock.recv(1024).decode('utf-8')

print(result)

sock.close()
