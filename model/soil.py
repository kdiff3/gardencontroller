##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import sys
import time
import os
import threading
from miflora.miflora_poller import *
from btlewrap.bluepy import BluepyBackend
from miflora import miflora_scanner

class Soil:
    def __init__(self, mac, max_moisture):
        self.max_moisture = max_moisture
        self.mac = mac
        self.soil_temperature_lock = threading.Lock()
        self.soil_moisture_lock = threading.Lock()
        self.soil_luminocity_lock = threading.Lock()
        self.soil_battery_lock = threading.Lock()
        try:
            self.poller = MiFloraPoller(mac, BluepyBackend)
            self.soil_temperature = self.__temperature()
            self.soil_moisture = self.__moisture()
            self.soil_luminocity = self.__luminocity()
            self.soil_battery = self.__battery()
            self.online = True
        except:
            self.online = False
            self.__scan()
        self.active = True
        self.timer_thread = threading.Thread(target=self.timerThread, daemon=True)
        self.timer_thread.start()

    def __del__(self):
        self.active = False

    def timerThread(self):
        while self.active:
            try:
                self.poller = MiFloraPoller(self.mac, BluepyBackend)
                with self.soil_temperature_lock:
                    self.soil_temperature = self.__temperature()
                with self.soil_moisture_lock:
                    self.soil_moisture = self.__moisture()
                with self.soil_luminocity_lock:
                    self.soil_luminocity = self.__luminocity()
                with self.soil_battery_lock:
                    self.soil_battery = self.__battery()
                self.online = True
            except:
                self.online = False
                self.__scan()
            time.sleep(60)

    def is_online(self):
        return self.online

    def temperature(self):
        with self.soil_temperature_lock:
            return self.soil_temperature

    def moisture(self):
        with self.soil_moisture_lock:
            return self.soil_moisture

    def luminocity(self):
        with self.soil_luminocity_lock:
            return self.soil_luminocity

    def battery(self):
        with self.soil_battery_lock:
            return self.soil_battery

    def __temperature(self):
        return self.poller.parameter_value("temperature")

    def __moisture(self):
        return self.poller.parameter_value(MI_MOISTURE)

    def __luminocity(self):
        return self.poller.parameter_value(MI_LIGHT)

    def __battery(self):
        return self.poller.parameter_value(MI_BATTERY)

    def __scan(args):
        try:
            miflora_scanner.scan(BluepyBackend, 10)
        except:
            os.system('/usr/bin/hcitool lescan')
