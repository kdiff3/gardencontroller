##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

class PumpGuard:
    def __init__(self, cistern, soil, battery, pump_in, pump_out):
        self.cistern = cistern
        self.soil = soil
        self.battery = battery
        self.pump_in = pump_in
        self.pump_out = pump_out

    def on(self):
        if self.__cistern_full() or self.__battery_level_inacceptable():
            self.pump_in.disable()
        if (not self.__cistern_full()) and self.__battery_level_acceptable():
            self.pump_in.enable()

    def off(self):
        if self.__cistern_empty() or (not self.__moisture_level_acceptable()):
            self.pump_out.disable()
        else:
            self.pump_out.enable()

    def __cistern_empty(self):
        return(self.cistern.distance() >= (self.cistern.height - 1))

    def __cistern_full(self):
        return(self.cistern.distance() <= 4.0)

    def __moisture_level_acceptable(self):
        return(self.soil.moisture() <= self.soil.max_moisture)

    def __battery_level_inacceptable(self):
        if self.__battery_present():
            return(self.battery.charge_status() <= 20)
        else:
            return True

    def __battery_level_acceptable(self):
        if self.__battery_present():
            return(self.battery.charge_status() > 50)
        else:
            return True

    def __battery_present(self):
        return(self.battery.voltage() > 2.0)
