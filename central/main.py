import socket
import json
import sys
import select

with open("../configuracao_sala_01.json", encoding='utf-8') as config_json:
    data = json.load(config_json)

def init():
    for index in range(len(data['servidores_distribuidos'])):
        room_number_ip[str(index)] = data['servidores_distribuidos'][index]["ip"]


def connect():
    room_socket, room_ip = server.accept()
    receiver.append(room_socket)
    rooms.append(room_socket)
    room_ip_socket[room_ip[0]] = room_socket
    print(f"Connected to: {room_ip[0]}")

def receive_message(connection):
    msg = connection.recv(1024).decode("utf-8")
    print(f"[SALA]: {msg}")

def send_message(connection):
    msg = input()

    room_ip = room_number_ip[msg[0]]
    room_socket = room_ip_socket[room_ip]

    print("Mensagem: ")
    msg = connection.readline()

    room_socket.sendall(msg.encode("utf-8"))

PORT = data['servidor_central']['porta']
IP = data['servidor_central']['ip']
src = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


receiver = [sys.stdin, server]
rooms = []
room_number_ip = {}
room_ip_socket = {}

init()

server.bind(src)
server.listen(5)

try:
    while True:
        inputs, _, _ = select.select(receiver, [], [])
        for connection in inputs:
            if connection is server:
                connect()
            elif isinstance(connection, socket.socket):
                receive_message(connection)
            else:
                send_message(connection)

except KeyboardInterrupt:
    print("Finalizando...")
finally:
    server.close()
