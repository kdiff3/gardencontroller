import sys
import os

from views.clientdatasocketadapter import *

class ConsoleView:
    def __init__(self, config):
        self.config = config
        self.adapter = clientDataSocketAdapter()
        self.view_data = self.adapter.get_view_data()
        print("Welcome to Gardencontroller Console Printer")

    def update(self):
        self.view_data = self.adapter.get_view_data()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.__print_timer_status()
        self.__print_moist_sensor_status()
        self.__print_cistern()
        self.__print_battery()
        self.__print_source()
        self.__print_pumps()
        self.__print_soil()

    def __print_soil(self):
        print("Soil Sensor Bat.  = %.1f %%" % self.view_data["soil_battery"])
        print("Soil moisture     = %.1f %%" % self.view_data["soil_moisture"])
        print("Soil temperature  = %.1f C" % self.view_data["soil_temperature"])
        print("Soil luminocity   = %.1f lx" % self.view_data["soil_luminocity"])

    def __print_pumps(self):
        print("Pump (in)         = %r (%r)" % (self.view_data["pump_in_status"], self.view_data["pump_in_enabled"]))
        print("Pump (out)        = %r (%r)" % (self.view_data["pump_out_status"], self.view_data["pump_out_enabled"]))

    def __print_source(self):
        if (self.view_data["source_wet"]):
            print("Source            = wet")
        else:
            print("Source            = dry")

    def __print_battery(self):
        print("Battery voltage   = %.1f v" % self.view_data["battery_voltage"])
        print("Battery capacity  = %.1f %%" % self.view_data["battery_charge_status"])
        print("Power Consumption = %.1f W" % self.view_data["power_consumption"])

    def __print_cistern(self):
        print("Fill              = %.1f l" % self.view_data["cistern_level"])
        print("Distance          = %.1f cm" % self.view_data["cistern_distance"])

    def __print_moist_sensor_status(self):
        if not self.view_data["soil_is_online"]:
            print("Soil sensor is offline!")

    def __print_timer_status(self):
        if self.view_data["water_timer_on"]:
            print("Watering is ", end='')
            if not self.view_data["pump_out_enabled"]:
                print("not ", end='')
            print("in progress for %.1f minutes" % self.view_data["water_timer_remaining_time"])
        else:
            print("Next watering in %.1f minutes" % self.view_data["water_timer_remaining_time"])
