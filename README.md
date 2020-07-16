# gardencontroller - Software for watering your turf!

Well, just put together a couple of components:

Main controller : 
https://www.raspberrypi.org/products/raspberry-pi-4-model-b/

Some relays for controlling the pumps:
https://wiki.52pi.com/index.php/DockerPi_4_Channel_Relay_SKU:_EP-0099

HC-SR04 for monitoring the water level in the cistern:
https://www.adafruit.com/product/3942

INA219 for monitoring the battery:
https://www.adafruit.com/product/904

YL-38 for monitoring whether a pump is really under water:
https://create.arduino.cc/projecthub/chocochunks/yl-38-moisture-meter-yl-69-sensor-290d88

Xiaomi Mi Flora for monitoring the soil:
https://github.com/open-homeautomation/miflora/blob/master/README.md

## Functionality

Gardencontroller is a framework for controlling up to four pumps that can water your soil, turf, flowers, vegetables (you name it). It is optimized for being battery powered, which is a fixed requirement for solar powered solutions. Gardencontroller can also get water from a not active source (e.g., pond, gutter drainage). It features several backends for monitoring (console, mail, MQTT).

## Dependencies

Uses Raspian : https://www.raspberrypi.org/downloads/raspberry-pi-os/

Please note that Python 3 needs to be system default (use update-alternatives):
https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux

The following libraries need to be installed:

	pip install pyyaml
	pip install smbus
	pip install pi-ina219
	pip install btlewrap
	pip install bluepy
	pip install miflora
	pip install gpiozero
	pip install paho-mqtt

The systemd script uses screen.

## License

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

[![Foo](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
