import RPi.GPIO as GPIO
import socket

class Controller():
    data: dict
    server: socket
    occupation: int
    security_alarm_status: bool
    fire_alarm_status: bool

    def __init__(self, data, server):
        self.data = data
        self.server = server
        self.occupation = 0
        self.security_alarm_status = False
        self.fire_alarm_status = False

        GPIO.add_event_detect(self.data['inputs'][4]['gpio'], GPIO.RISING, callback=self._increase_occupation)
        GPIO.add_event_detect(self.data['inputs'][5]['gpio'], GPIO.RISING, callback=self._decrease_occupation)

        GPIO.add_event_detect(self.data['inputs'][0]['gpio'], GPIO.RISING, callback=self._notify_security_alarm)
        GPIO.add_event_detect(self.data['inputs'][2]['gpio'], GPIO.RISING, callback=self._notify_security_alarm)
        GPIO.add_event_detect(self.data['inputs'][3]['gpio'], GPIO.RISING, callback=self._notify_security_alarm)

        GPIO.add_event_detect(self.data['inputs'][1]['gpio'], GPIO.RISING, callback=self._notify_fire_alarm)

    def _increase_occupation(self, pin):
        self.occupation = self.occupation + 1

    def _decrease_occupation(self, pin):
        if self.occupation > 0:
            self.occupation = self.occupation - 1

    def _notify_security_alarm(self, pin):
        if self.security_alarm_status:
            self.server.sendall("2".encode("utf-8"))

    def _notify_fire_alarm(self, pin):
        if self.fire_alarm_status:
            self.server.sendall("3".encode("utf-8"))

    def _execute_option(self, chooses):
        if chooses[0] ==  "1":
            return self._execute_consult()
        elif chooses[0] ==  "2":
            self._execute_change(chooses[1:])
        elif chooses[0] ==  "3":
            return str(self.occupation)
        elif chooses[0] ==  "4":
            return self._update_security_alarm(chooses[1:])
        elif chooses[0] ==  "5":
            return self._update_fire_alarm(chooses[1:])
        elif chooses[0] ==  "6":
            return self._execute_alarm()

    def _execute_consult(self):
        result = ""
        for output in self.data["outputs"]:
            state = "ON" if GPIO.input(output['gpio']) == 1 else "OFF"
            result = result + f"[{output['tag']}]: {state}" + "\n"
        for input in self.data["inputs"]:
            state = "ON" if GPIO.input(input['gpio']) == 1 else "OFF"
            result = result + f"[{input['tag']}]: {state}" + "\n"
        return result

    def _execute_change(self, chooses):
        if chooses[0] ==  "1":
            self._execute_change_lamps(chooses[1:])
        elif chooses[0] ==  "2":
            self._execute_on_off(chooses[1:], [self.data["outputs"][2]["gpio"]])
        elif chooses[0] ==  "3":
            self._execute_on_off(chooses[1:], [self.data["outputs"][3]["gpio"]])

    def _execute_change_lamps(self, chooses):
        if chooses[0] ==  "1":
            self._execute_on_off(chooses[1:], [self.data["outputs"][0]["gpio"]])
        elif chooses[0] ==  "2":
            self._execute_on_off(chooses[1:], [self.data["outputs"][1]["gpio"]])
        elif chooses[0] ==  "3":
            self._execute_on_off(chooses[1:], [self.data["outputs"][0]["gpio"], self.data["outputs"][1]["gpio"]])

    def _execute_change_projector(self, chooses):
        self._execute_on_off(chooses[1:], [self.data["outputs"][0]["gpio"]])

    def _execute_on_off(self, chooses, outputs):
        if chooses[0] ==  "1":
            for output in outputs:
                GPIO.output(output, True)
        elif chooses[0] ==  "2":
            for output in outputs:
                GPIO.output(output, False)

    def _update_security_alarm(self, chooses):
        if chooses[0] == "1":
            self.security_alarm_status = True
        elif chooses[0] == "2":
            GPIO.output(self.data['outputs'][4]['gpio'], False)
            self.security_alarm_status = False

    def _update_fire_alarm(self, chooses):
        if chooses[0] == "1":
            self.fire_alarm_status = True
            current_value = GPIO.input(self.data['inputs'][1]['gpio'])
            if current_value:
                self._notify_fire_alarm(self.data['inputs'][1]['gpio'])
        elif chooses[0] == "2":
            GPIO.output(self.data['outputs'][4]['gpio'], False)
            self.fire_alarm_status = False

    def _execute_alarm(self):
        GPIO.output(self.data['outputs'][4]['gpio'], True)