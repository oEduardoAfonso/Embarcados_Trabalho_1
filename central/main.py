import socket
import json
import sys
import select
from view import View

with open("./configuracao_sala_01.json", encoding='utf-8') as config_json:
    data = json.load(config_json)

def init():
    server.bind(src)
    server.listen()

    room_number_ip["1"] = data['servidores_distribuidos'][0]["ip"]
    room_number_ip["3"] = data['servidores_distribuidos'][1]["ip"]
    room_number_ip["4"] = data['servidores_distribuidos'][2]["ip"]

    view._show_room_menu(room_number_ip, room_ip_socket)


def find_number_by_ip(room_ip):
    for number in room_number_ip:
        if room_number_ip[number] == room_ip:
            return number

def find_ip_by_socket(socket):
    for ip in room_ip_socket:
        if room_ip_socket[ip] == socket:
            return ip

def find_number_by_socket(socket):
    ip =  find_ip_by_socket(socket)
    return find_number_by_ip(ip)


def connect():
    room_socket, room_ip_port = server.accept()
    receiver.append(room_socket)
    rooms.append(room_socket)

    room_ip_socket[room_ip_port[0]] = room_socket
    room_number = find_number_by_ip(room_ip_port[0])

    view._clean()
    print(f"Connected to room: {room_number}")
    view._show_room_menu(room_number_ip, room_ip_socket)

def receive_message(connection):
    msg = connection.recv(1024).decode("utf-8")
    if msg:
        print(f"[SALA]: {msg}")
    else:
        view._clean()
        print(f"Closing connection to room: {find_number_by_socket(connection)}")
        receiver.remove(connection)
        rooms.remove(connection)
        del room_ip_socket[find_ip_by_socket(connection)]
        connection.close()
        view._show_room_menu(room_number_ip, room_ip_socket)

def send_message(connection):
    msg = input()

    room_ip = room_number_ip[msg[0]]
    room_socket = room_ip_socket[room_ip]

    chooses = view._show_menu(connection)
    print(chooses)
    view._clean()
    room_socket.sendall(chooses.encode("utf-8"))

PORT = data['servidor_central']['porta']
IP = data['servidor_central']['ip']
src = (IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


receiver = [sys.stdin, server]
rooms = []
room_number_ip = {}
room_ip_socket = {}
view = View()
init()

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
                view._show_room_menu(room_number_ip, room_ip_socket)

except KeyboardInterrupt:
    print("Application Closing")
finally:
    server.close()
