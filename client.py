#!/usr/bin/env py3

import socket
import json
from client_gui import *
from _thread import *

class Client():
    def __init__(self):
        self.gui = ClientGUI()
        self.gui.init_gui()
        self.sock = socket.socket()
        self.sock.settimeout(300)

    def __del__(self):
        self.gui.g_input("Press any key to exit...", 3)
        self.gui.del_gui()

    def __receive(self):
        self.gui.g_print("Receiver started...", 3)
        while True:
            try:
                data = self.sock.recv(256).decode()
                if not data:
                    break
                if "~//onl" in data:
                    data = data[7:]
                    data = json.loads(data)
                    self.gui.g_onliners(data)
                    self.gui.g_input_clear()
                    continue
                self.gui.g_print(data)
                self.gui.g_input_clear()
            except Exception as e:
                self.gui.g_print("Error while receiving: {}".format(e), 4)
                break
        self.gui.g_print("Receiver stopped...", 3)

    def _pick_name(self):
        while True:
            name = self.gui.g_input("We need a name", 3)
            if not name:
                name = ''
            if 0 < len(name) <= 10:
                return name
            self.gui.g_print("Name must be from1  to 10 chars lenght..", 4)


    def start(self):
        host = self.gui.g_input("Enter IP address", 3)
        self.gui.g_print(host)
        try:
            self.sock.connect((host, 17117))
        except ConnectionRefusedError:
            self.gui.g_print("Server doesn't respond", 4)
        except Exception as e:
            self.gui.g_print("Cant connect cause: {}".format(e), 4)
        else:
            try:
                start_new_thread(self.__receive, ())
            except Exception as e:
                self.gui.g_print("Receiver starting failed cause: {}".format(e), 4)
            else:
                self.gui.g_print("Connected! Type //exit to exit", 3)
                name = self._pick_name()
                self.gui.g_print("Welcome to server, {}!".format(name), 3)
                self.sock.send("~//name {}".format(name).encode())
                while True:
                    data = self.gui.g_input()
                    if not data or data == "\n":
                        continue
                    if data == "//exit":
                        break
                    self.gui.g_print("{}: {}".format(name, data))
                    data = '!' + data
                    try:
                        self.sock.send(data.encode())
                    except BrokenPipeError:
                        self.gui.g_print("Something wrong with this server...", 4)
                        break
            finally:
                self.__del__()
# -------------------------------------------------------------------------------------------------------------------------------------

client = Client()
client.start()
