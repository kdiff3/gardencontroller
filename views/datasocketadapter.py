import time
import sys
import os
import threading
import socket
import pickle

from model.cistern import *
from model.battery import *
from model.pump import *
from model.soil import *

HEADERSIZE = 10

class dataSocketAdapter:
    def __init__(self, config, cistern, battery, pump_out, pump_in, soil, water_timer, source):
        self.config = config
        self.cistern = cistern
        self.battery = battery
        self.pump_out = pump_out
        self.pump_in = pump_in
        self.soil = soil
        self.water_timer = water_timer
        self.source = source
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 32000))
        self.active = True
        self.timer_thread = threading.Thread(target=self.timerThread, daemon=True)
        self.timer_thread.start()

    def __del__(self):
        self.active = False
        self.server_socket.close()

    def timerThread(self):
        while self.active:
            self.server_socket.listen(5)
            clientsocket, address = self.server_socket.accept()
            print(f"Client connected from {address}!")
            socket_thread = threading.Thread(target=self.socketThread, daemon=True, args=(clientsocket,))
            socket_thread.start()

    def socketThread(self, clientsocket):
        try:
            while True:
                clientsocket.send(self.update())
                time.sleep(self.config["view_update_intervall"])
        except:
            print("Client closed connection!")

    def update(self):
        display = {
            "water_timer_on": self.water_timer.on,
            "water_timer_remaining_time": (self.water_timer.remaining_time / 60),
            "cistern_level": self.cistern.level(),
            "cistern_distance": self.cistern.distance(),
            "cistern_height": self.cistern.height,
            "battery_voltage": self.battery.voltage(),
            "battery_charge_status": self.battery.charge_status(),
            "power_consumption": (self.battery.power()/1000),
            "pump_in_status": self.pump_in.status,
            "pump_in_enabled": self.pump_in.enabled,
            "pump_out_status": self.pump_out.status,
            "pump_out_enabled": self.pump_out.enabled,
            "soil_is_online": self.soil.is_online(),
            "soil_battery": self.soil.battery(),
            "soil_moisture": self.soil.moisture(),
            "soil_temperature": self.soil.temperature(),
            "soil_luminocity": self.soil.luminocity(),
            "source_wet": self.source.wet()
        }
        message = pickle.dumps(display)
        return(bytes(f"{len(message):<{HEADERSIZE}}", 'utf-8') + message)
