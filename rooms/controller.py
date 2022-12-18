import RPi.GPIO as GPIO

class Controller():
    data: dict

    def __init__(self, data):
        self.data = data

    def _execute_option(self, chooses):
        if chooses[0] ==  "1":
            print("to-do")
        elif chooses[0] ==  "2":
            self._execute_change(chooses[1:])

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
