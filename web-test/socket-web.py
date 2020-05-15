import socket

host = ''
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

while True:
    conn, caddr = sock.accept()
    print ("Connection from: ", caddr)
    req = conn.recv(1024).decode('utf-8')
    print (req)
    conn.sendall("""HTTP/1.0 200 OK
Content-Type: text/html

<html>
<head>
<title>Success</title>
</head>
<body>
Boo!
</body>
</html>
""".encode('utf-8'))
    conn.close()