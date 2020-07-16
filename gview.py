#!/usr/bin/python3

##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import sys
import os
import yaml
import argparse

from views.consoleview import *
from views.mailview import *
from views.mqttview import *

def main():
    parser = argparse.ArgumentParser(description='Starter for Gardencontroller views')
    parser.add_argument("--console", help="Start console", action="store_true", default=False)
    parser.add_argument("--mail", help="Start mail agent", action="store_true", default=False)
    parser.add_argument("--mqtt", help="Start mqtt backend", action="store_true", default=False)
    args = parser.parse_args()

    with open('/etc/gcontroller.yaml') as config_file:
        if args.console:
            view = ConsoleView(yaml.load(config_file, Loader=yaml.FullLoader))
        if args.mail:
            view = MailView(yaml.load(config_file, Loader=yaml.FullLoader))
        if args.mqtt:
            view = MqttView(yaml.load(config_file, Loader=yaml.FullLoader))

    del args
    del parser

    try:
        while True:
            view.update()

    except KeyboardInterrupt:
        del view


if __name__ == '__main__':
    main()
