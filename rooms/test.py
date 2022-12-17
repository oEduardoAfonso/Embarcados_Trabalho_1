import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(25, GPIO.OUT)

state = False

while(True):
    state = not state
    GPIO.output(25, state)
    time.sleep(1)
