from Сервера_и_слиенты.problem_4.go_to_network import *
import time

client = Client('127.0.0.1', 9090)
print("connected")

for i in range(10):
    client.send(str(i))
    time.sleep(1)
client.send("end")
print("end")
