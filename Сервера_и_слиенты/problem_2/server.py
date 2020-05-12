import socket

sock = socket.socket()

sock.bind(('', 9090))

sock.listen(1)

while True:
    conn, addr = sock.accept()

    client_data = conn.recv(1024)
    client_int = int(client_data.decode('utf-8'))

    conn.send(str(client_int**2).encode('utf-8'))

    conn.close()
