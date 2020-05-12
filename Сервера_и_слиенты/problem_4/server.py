from Сервера_и_слиенты.problem_4.go_to_network import *


server = Server(9090)

while True:
    server.accept()

    while True:
        message = server.receive_string()

        if message:

            print(f'{server.addr}: {message}')

        if message == "end":
            break

    server.close()
