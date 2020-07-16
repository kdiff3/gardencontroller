##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import RPi.GPIO as GPIO
import time
import threading
import queue

class Cistern:
    def __init__(self, length, depth, height):
        self.length = length
        self.depth = depth
        self.height = height
        self.gpio_trigger = 18 # GPIO 18
        self.gpio_echo = 24 # GPIO 24
        self.start_time = time.time()
        self.stop_time = time.time()
        self._lock = threading.Lock()
        self.distance_internal = 8
        self.active = True
        self.timer_thread = threading.Thread(target=self.timerThread, daemon=True)
        self.timer_thread.start()

    def __del__(self):
        self.active = False
        GPIO.cleanup()

    def level(self):
        return round((((self.height-self.distance())*self.length*self.depth)/1000), 2)

    def distance(self):
        with self._lock:
            return(self.distance_internal)

    def timerThread(self):
        while self.active:
            with self._lock:
                measurement = self.__distance()
                if (measurement >= 0) and (measurement <= self.height):
                    self.distance_internal = round(measurement, 2)
            time.sleep(1)

    def __distance(self):
        try:
            self.__setup_gpio()
            self.__send_ping()
            self.__wait_for_ping()
        except:
            GPIO.cleanup()
        TimeElapsed = self.stop_time - self.start_time
        return ((TimeElapsed * 34300) / 2)

    def __setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

    def __wait_for_ping(self):
        loops = 0
        while (GPIO.input(self.gpio_echo) == 0) and (loops < 2000):
            self.start_time = time.time()
            loops += 1
            time.sleep(1/10000.0)
        loops = 0
        while (GPIO.input(self.gpio_echo) == 1) and (loops < 2000):
            self.stop_time = time.time()
            loops += 1
            time.sleep(1/10000.0)

    def __send_ping(self):
        GPIO.output(self.gpio_trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)
