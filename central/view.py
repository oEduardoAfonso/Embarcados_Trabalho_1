class View():
    security_alarm_status: bool
    fire_alarm_status: bool

    def __init__(self):
        self.security_alarm_status = False
        self.fire_alarm_status = False

    def _clean(self):
        for i in range(50):
            print()

    def _show_first_menu(self):
        security_alarm_status_str = "ON" if self.security_alarm_status else "OFF"
        fire_alarm_status_str = "ON" if self.fire_alarm_status else "OFF"
        print("\nChoose an option:")
        print("[1] - Access Room")
        print(f"[2] - Change security alarm system ({security_alarm_status_str})")
        print(f"[3] - Change fire alarm system ({fire_alarm_status_str})\n")

    def _show_menus(self, connection, room_number_ip, room_ip_socket, room_number_occupation):
        return self._show_room_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)

    def _show_room_menu(self, connection, room_number_ip, room_ip_socket, room_number_occupation):
        if len(room_ip_socket) == 0:
            print("\nNO CONNECTIONS YET!\n")
        else:
            print("\nChoose a room to access:")
            for number in room_number_ip:
                if room_number_ip[number] in room_ip_socket:
                    print(f"[{number}] - Room {number} (Occupation: {room_number_occupation[number]} people)")
            total_occupation = 0
            for number in room_number_occupation:
                total_occupation = total_occupation + int(room_number_occupation[number])
            print("\n[0] - Go back to last menu\n")
            print(f"Number of people at the building: [{total_occupation}]\n")


            msg = connection.readline()

            self._clean()
            if msg[0] != "0":
                return msg[0] + self._show_consult_or_change_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)


    def _show_consult_or_change_menu(self, connection, room_number_ip, room_ip_socket, room_number_occupation):
        print("\nDo you want to consult or change the room?")
        print("[1] - Consult")
        print("[2] - Change")
        print("\n[0] - Go back to last menu\n")

        msg = connection.readline()

        self._clean()
        if msg[0] ==  "1":
            return "1"
        elif msg[0] ==  "2":
            return "2" + self._show_change_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)
        elif msg[0] ==  "0":
            return self._show_room_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)

    def _show_change_menu(self, connection, room_number_ip, room_ip_socket, room_number_occupation):
        print("\nWhich device you'd like to change?")
        print("[1] - Lamps")
        print("[2] - Projector")
        print("[3] - Air Conditioner")
        print("\n[0] - Go back to last menu\n")

        msg = connection.readline()

        self._clean()
        if msg[0] ==  "1":
            return "1" + self._show_lamp_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)
        elif msg[0] ==  "2":
            return "2" + self._show_on_or_off_menu(connection)
        elif msg[0] ==  "3":
            return "3" + self._show_on_or_off_menu(connection)
        elif msg[0] ==  "0":
            return self._show_consult_or_change_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)

    def _show_lamp_menu(self, connection, room_number_ip, room_ip_socket, room_number_occupation):
        print("\nWhich lamp you'd like to change?")
        print("[1] - Lamp 1")
        print("[2] - Lamp 2")
        print("[3] - Both")
        print("\n[0] - Go back to last menu\n")

        msg = connection.readline()

        self._clean()
        if msg[0] != "0":
            return msg[0] + self._show_on_or_off_menu(connection)
        elif msg[0] ==  "0":
            return self._show_change_menu(connection, room_number_ip, room_ip_socket, room_number_occupation)


    def _show_on_or_off_menu(self, connection):
        print("\nWould you like to turn it on or off?")
        print("[1] - On")
        print("[2] - Off")

        msg = connection.readline()

        self._clean()

        return msg[0]
