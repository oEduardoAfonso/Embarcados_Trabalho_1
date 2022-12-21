import io
import socket
import select
import sys
import json
import time
import RPi.GPIO as GPIO
from rooms.controller import Controller

def mainRoom(room_number, server_number):

    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for output in data['outputs']:
            GPIO.setup(output['gpio'], GPIO.OUT)

        for input in data['inputs']:
            GPIO.setup(input['gpio'], GPIO.IN)

        is_connected = False

        while not is_connected:
            print("Trying to connect...")
            try:
                server.connect(dest)
                is_connected = True
                print("Connected to server")
            except ConnectionRefusedError:
                time.sleep(1)

    json_file = "./configuracao_sala_01.json" if int(room_number) % 2 == 1 else "./configuracao_sala_02.json"
    with io.open(json_file, encoding='utf-8') as config_json:
        data = json.load(config_json)

    IP = data['servidores'][int(server_number) - 1]['ip']
    PORT = data['servidores'][int(server_number) - 1]['porta']


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (IP, PORT)

    init()

    controller = Controller(data, server)

    try:
        while True:
            inputs, _, _ = select.select([sys.stdin, server], [], [])

            for connection in inputs:
                if connection is server:
                    msg = connection.recv(1024).decode("utf-8")
                    if msg:
                        result = controller._execute_option(msg)
                        if result:
                            server.send(bytes(result, 'utf-8'))
                    else:
                        server.close()
                else:
                    msg = connection.readline()
                    server.send(bytes(msg, 'utf-8'))
    except (KeyboardInterrupt, ValueError):
        print("Application Closing")
    finally:
        GPIO.cleanup()
        server.close()
