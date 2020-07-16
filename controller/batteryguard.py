##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import os
from gpiozero import Button

class BatteryGuard:
    def __init__(self, battery):
        self.battery = battery
        self.stop_button = Button(26) # GPIO 26

    def on(self):
        self.off()

    def off(self):
        self.check_stop_button()

    def check_stop_button(self):
        if self.stop_button.is_pressed:
            print("System is powering down!")
            os.system("poweroff")
