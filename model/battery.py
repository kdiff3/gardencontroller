##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

from ina219 import INA219
from ina219 import DeviceRangeError
import time
import threading

class Battery:
    def __init__(self):
        self.shunt_ohms = 0.1
        self.max_expected_amps = 0.010
        self.ina = INA219(self.shunt_ohms, self.max_expected_amps)
        self.ina.configure(self.ina.RANGE_16V, self.ina.GAIN_1_40MV)
        self.charge_lookup = {
            12.60 : 100,
            12.48 : 90,
            12.36 : 80,
            12.24 : 70,
            12.12 : 60,
            12.00 : 50,
            11.85 : 40,
            11.70 : 30,
            11.30 : 20,
            10.90 : 10,
            10.50 : 0,
            0.00 : 0
        }
        self.active = True
        self.timer_thread = threading.Thread(target=self.timerThread, daemon=True)
        self.timer_thread.start()
        self.power_internal = 0

    def __del__(self):
        self.active = False

    def timerThread(self):
        while self.active:
            accumulator = 0
            divider = 0
            for i in range(0, 100):
                try:
                    accumulator += self.ina.power()
                    divider += 1
                except:
                    accumulator += 0
                time.sleep(1/100.0)
            if(divider == 0):
                divider = 1
            self.power_internal = (accumulator/divider)


    def voltage(self):
        return self.ina.voltage()

    def current(self):
        try:
            return self.ina.current()
        except DeviceRangeError as e:
            return 0

    def power(self):
        return self.power_internal

    def charge_status(self):
        return self.__get_nearest_element(self.charge_lookup, self.voltage())

    def __get_nearest_element(self, dictionary, search_key):
        return (dictionary.get(search_key) or dictionary[ min(dictionary.keys(), key = lambda key: abs(key-search_key))])
