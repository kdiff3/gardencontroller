#!/usr/bin/python3

##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import time
import sys
import os
import yaml

from model.cistern import *
from model.battery import *
from model.pump import *
from model.soil import *
from model.source import *

from views.datasocketadapter import *

from controller.timeroperator import *
from controller.batteryguard import *
from controller.pumpguard import *

def main():
    with open('/etc/gcontroller.yaml') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    # Model
    cistern = Cistern(config["cistern_length"], config["cistern_depth"], config["cistern_height"])
    battery = Battery()
    pump_out = Pump(1)
    pump_out.enable()
    pump_in = Pump(2)
    pump_in.enable()
    source = Source(pump_in)
    soil = Soil(config["soil_mac"], config["soil_max_moisture"])

    # Controller
    battery_timer = TimerOperator(BatteryGuard(battery), (1/60), 1)
    pump_safety_timer = TimerOperator(PumpGuard(cistern, soil, battery, pump_in, pump_out), (1/60), 1)
    water_timer = TimerOperator(pump_out, config["water_timer_gap"], config["water_timer_duration"])

    # View
    view_socket_adapter = dataSocketAdapter(config, cistern, battery, pump_out, pump_in, soil, water_timer, source)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to Gardencontroller v1.0")

    try:
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        print("Keyboard interrupt -> exiting!")
        del view_socket_adapter
        del pump_safety_timer
        del water_timer
        del battery_timer
        del source
        del pump_in
        del pump_out
        del battery
        del cistern
        del soil

if __name__ == '__main__':
    main()
