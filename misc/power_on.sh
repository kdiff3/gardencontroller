#!/bin/bash

/power_off.sh

/opt/vc/bin/tvservice -o
echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind

cd /gardencontroller/
screen -d -S gcontroller -m ./gcontroller.py
sleep 20
screen -d -S gmailer -m ./gview.py --mail
sleep 20
screen -d -S gmqtt -m ./gview.py --mqtt
