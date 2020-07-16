##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import time as t
import smbus
import sys

import threading

class Pump:
    def __init__(self, number):
        if number not in range(1, 4):
            sys.exit(-1)
        self.number = number
        self._device_addr = 0x10
        self._bus = smbus.SMBus(1)
        self._lock = threading.Lock()
        self.off()
        self.disable()

    def __del__(self):
        self.off()
        self.disable()

    def on(self):
        with self._lock:
            self.status = True
            if(self.enabled):
                self.__on()

    def __on(self):
        self._bus.write_byte_data(self._device_addr, self.number, 0xFF)

    def off(self):
        with self._lock:
            self.__off()
            self.status = False

    def __off(self):
        self._bus.write_byte_data(self._device_addr, self.number, 0x00)

    def disable(self):
        with self._lock:
            self.__off()
            self.enabled = False

    def enable(self):
        with self._lock:
            if self.status:
                self.__on()
            self.enabled = True
