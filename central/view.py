class View():

    def _clean(self):
        for i in range(50):
            print()

    def _show_menu(self, connection):
        return self._show_consult_or_change_menu(connection)

    def _show_consult_or_change_menu(self, connection):
        print("Do you want to consult or change the room?")
        print("[1] - Consult")
        print("[2] - Change")

        msg = connection.readline()

        if msg[0] ==  "1":
            return "1"
        elif msg[0] ==  "2":
            return "2" + self._show_change_menu(connection)

    def _show_change_menu(self, connection):
        print("Which device you'd like to change?")
        print("[1] - Lamps")
        print("[2] - Projector")
        print("[3] - Air Conditioner")

        msg = connection.readline()

        if msg[0] ==  "1":
            return "1" + self._show_lamp_menu(connection)
        elif msg[0] ==  "2":
            return "2" + self._show_on_or_off_menu(connection)
        elif msg[0] ==  "3":
            return "3" + self._show_on_or_off_menu(connection)

    def _show_lamp_menu(self, connection):
        print("Which lamp you'd like to change?")
        print("[1] - Lamp 1")
        print("[2] - Lamp 2")
        print("[3] - Both")

        msg = connection.readline()

        return msg[0] + self._show_on_or_off_menu(connection)

    def _show_on_or_off_menu(self, connection):
        print("Would you like to turn it on or off?")
        print("[1] - On")
        print("[2] - Off")

        msg = connection.readline()

        return msg[0]

    def _show_room_menu(self, room_number_ip, room_ip_socket):
        if len(room_ip_socket) == 0:
            self._clean()
            print("No connections made.")
        else:
            print("Choose a room to control:")
            for number in room_number_ip:
                if room_number_ip[number] in room_ip_socket:
                    print(f"[{number}] - Room {number}")
