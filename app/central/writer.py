import csv
import os
from datetime import datetime

class Writer():

    def __init__(self):
        if os.path.exists('./log.csv'):
            os.remove('./log.csv')
        header = ["action", "datetime"]
        with open('log.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(header)

    def _write_row(self, command):
        with open('log.csv', 'a', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow([command, datetime.now()])

    def _to_command(self, commands):
        return self._get_first_command(commands)

    def _get_first_command(self, commands):
        if commands[0] == "4":
            return "Turned security alarm system " + self._get_on_off(commands[1:])
        elif commands[0] == "5":
            return "Turned fire alarm system " + self._get_on_off(commands[1:])
        else:
            return f"Accessed room number {commands[0]} " + self._get_consult_or_change(commands[1:])

    def _get_consult_or_change(self, commands):
        if commands[0] == "1":
            return "and consulted the status"
        elif commands[0] == "2":
            return "and turned " + self._get_device(commands[1:])

    def _get_device(self, commands):
        if commands[0] == "1":
            return self._get_lamp(commands[1:])
        elif commands[0] == "2":
            return "the \'Projetor Multimidia\' " + self._get_on_off(commands[1:])
        elif commands[0] == "3":
            return "the \'Ar-Condicionado (1º Andar)\' " + self._get_on_off(commands[1:])

    def _get_lamp(self, commands):
        if commands[0] == "1":
            return "the \'Lâmpada 1\' " + self._get_on_off(commands[1:])
        elif commands[0] == "2":
            return "the \'Lâmpada 2\' " + self._get_on_off(commands[1:])
        elif commands[0] == "3":
            return "both \'Lâmpadas\' " + self._get_on_off(commands[1:])

    def _get_on_off(self, commands):
        if commands[0] == "1":
            return "ON"
        elif commands[0] == "2":
            return "OFF"
