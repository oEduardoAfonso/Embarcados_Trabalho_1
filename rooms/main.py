import io
import socket
import select
import sys
import json
# import time
import RPi.GPIO as GPIO
from controller import Controller

def init():
    server.connect(dest)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for output in data['outputs']:
        GPIO.setup(output['gpio'], GPIO.OUT)

    for input in data['inputs']:
        GPIO.setup(input['gpio'], GPIO.IN)

with io.open("./configuracao_sala.json", encoding='utf-8') as config_json:
    data = json.load(config_json)

PORT = data['servidor_central']['porta']
IP = data['servidor_central']['ip']

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
