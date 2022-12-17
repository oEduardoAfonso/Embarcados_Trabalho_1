import socket
import select
import sys
import json
# import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(25, GPIO.OUT)

with open("../configuracao_sala_01.json", encoding='utf-8') as config_json:
    data = json.load(config_json)

PORT = data['servidor_central']['porta']
IP = data['servidor_central']['ip']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (IP, PORT)

server.connect(dest)

try:
    while True:
        inputs, _, _ = select.select([sys.stdin, server], [], [])
        for connection in inputs:
            if connection is server:
                msg = connection.recv(1024).decode("utf-8")
                if msg == "on\n":
                    GPIO.output(25, True)
                    print("Acendeu")
                else:
                    GPIO.output(25, False)
                    print(msg)


            else:
                msg = connection.readline()
                server.send(bytes(msg, 'utf-8'))
except KeyboardInterrupt:
    print("Finalizando...")
finally:
    server.close()

server.close()
