##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import RPi.GPIO as GPIO
from gpiozero import InputDevice
import time
import threading
import queue

class Source:
    def __init__(self, pump):
        self.pump = pump
        self.water_sensor = InputDevice(16) # GPIO 16
        self.active = True
        self.timer_thread = threading.Thread(target=self.timerThread, daemon=True)
        self.timer_thread.start()

    def __del__(self):
        self.active = False

    def wet(self):
        return(not self.water_sensor.is_active)

    def timerThread(self):
        while self.active:
            if self.wet():
                self.pump.on()
            else:
                time.sleep(10)
                self.pump.off()
        time.sleep(1)
