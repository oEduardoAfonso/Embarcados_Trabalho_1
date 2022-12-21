import socket
import io
import json
import sys
import select
import time
from central.view import View
from central.writer import Writer

def mainCentral(room_number):

    def init():
        server.bind(src)
        server.listen()

        index = 1
        for server_json in data['servidores']:
            print(f"index[{index}]: ip[{server_json['ip']}]")
            room_number_ip[str(index)] = server_json["ip"]
            index += 1

        view._clean()
        show_main_menu()


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

    def update_room_data():
        for room_number in room_number_ip:
            if room_number_ip[room_number] in room_ip_socket:
                room_ip = room_number_ip[room_number]
                room_socket = room_ip_socket[room_ip]

                room_socket.sendall("3".encode("utf-8"))
                occupation = room_socket.recv(1024).decode("utf-8")
                room_number_occupation[room_number] = occupation

                room_socket.sendall("7".encode("utf-8"))
                dht = room_socket.recv(1024).decode("utf-8")
                room_number_dht[room_number] = dht

    def show_main_menu():
        update_room_data()
        view._clean()
        view._show_first_menu(room_number_ip, room_ip_socket, room_number_occupation, room_number_dht)

    def connect():
        room_socket, room_ip_port = server.accept()
        receiver.append(room_socket)
        rooms.append(room_socket)

        room_ip_socket[room_ip_port[0]] = room_socket
        room_number = find_number_by_ip(room_ip_port[0])

        print(f"\nRoom number [{room_number}] connected.\nGetting DHT22 data...")
        time.sleep(1)

    def receive_message(connection):
        msg = connection.recv(1024).decode("utf-8")
        if msg:
            if msg[0] == "2":
                display_msg = f"Security alarm buzzer activated by room: {find_number_by_socket(connection)}"
                writer._write_row(display_msg)
                print(display_msg)
            elif msg[0] == "3":
                display_msg = f"Fire alarm buzzer activated by room: {find_number_by_socket(connection)}"
                writer._write_row(display_msg)
                print(display_msg)

            if msg[0] == "2" or msg[0] == "3":
                for room in rooms:
                    room.sendall("6".encode("utf-8"))

                print("\nPress [ENTER] to go back to menu")
                input()

        else:
            view._clean()
            print(f"Closing connection to room [{find_number_by_socket(connection)}]")
            receiver.remove(connection)
            rooms.remove(connection)
            number = find_number_by_socket(connection)
            del room_ip_socket[find_ip_by_socket(connection)]
            del room_number_occupation[number]
            connection.close()

    def send_message(connection):
        msg = input()
        view._clean()
        commands = None

        if msg:
            if msg[0] == "7":
                view._show_all_rooms_menu()
                all_rooms_command = input()
                all_rooms_message = ""

                if all_rooms_command[0] == "1":
                    all_rooms_message = "2131"
                elif all_rooms_command[0] == "2":
                    all_rooms_message = "9"
                else:
                    return

                for room in rooms:
                    room.sendall(all_rooms_message.encode("utf-8"))
                    room_response = room.recv(1024).decode("utf-8")

                if len(room_response) > 0:
                    view._clean()
                    print("All rooms were changed")
                    print("\nPress [ENTER] to go back to menu")
                    connection.readline()

            elif msg[0] == "8":
                if not view.security_alarm_status:
                    security_sensors_active = False
                    for room in rooms:
                        room.sendall("8".encode("utf-8"))
                        room_sensors_status = room.recv(1024).decode("utf-8")
                        if room_sensors_status[0] == "1":
                            security_sensors_active = True

                    if security_sensors_active:
                        print("[ERROR] Failed to activate security system\n[ERROR] There are motion sensors ON")
                        print("\nPress [ENTER] to go back to menu")
                        connection.readline()
                    else:
                        for room in rooms:
                            room.sendall("41".encode("utf-8"))
                        view.security_alarm_status = not view.security_alarm_status

                else:
                    for room in rooms:
                        room.sendall("42".encode("utf-8"))
                    view.security_alarm_status = not view.security_alarm_status

            elif msg[0] == "9":
                chooses = "5"

                view.fire_alarm_status = not view.fire_alarm_status

                chooses = chooses + ("1" if view.fire_alarm_status else "2")

                commands = chooses
                for room in rooms:
                    room.sendall(chooses.encode("utf-8"))
            else:
                chooses = view._show_menus(connection, msg[0])

                if chooses:
                    commands = msg[0] + chooses

                    room_ip = room_number_ip[msg[0]]
                    room_socket = room_ip_socket[room_ip]

                    view._clean()
                    room_socket.sendall(chooses.encode("utf-8"))

                    msg = room_socket.recv(1024).decode("utf-8")
                    if chooses[0] == "1":
                        print(f"Status Room [{find_number_by_ip(room_ip)}] :\n{msg}")
                    else:
                        print(msg)
                    print("\nPress [ENTER] to go back to menu")
                    connection.readline()
            if commands:
                writer._write_row(writer._to_command(commands))

    json_file = "./configuracao_sala_01.json" if int(room_number) % 2 == 1 else "./configuracao_sala_02.json"
    with io.open(json_file, encoding='utf-8') as config_json:
        data = json.load(config_json)

    IP = data['servidores'][int(room_number) - 1]['ip']
    PORT = data['servidores'][int(room_number) - 1]['porta']

    src = (IP, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)


    receiver = [sys.stdin, server]
    rooms = []
    room_number_ip = {}
    room_ip_socket = {}
    room_number_occupation = {}
    room_number_dht = {}
    view = View()
    writer = Writer()
    init()

    try:
        while True:
            show_main_menu()
            timeout = 2.0 if len(rooms) > 0 else None
            inputs, _, _ = select.select(receiver, [], [], timeout)

            for connection in inputs:
                if connection is server:
                    connect()
                elif isinstance(connection, socket.socket):
                    receive_message(connection)
                else:
                    send_message(connection)


    except (KeyboardInterrupt, OSError):
        print("Application Closing")
    finally:
        server.shutdown(socket.SHUT_RDWR)
        server.close()
