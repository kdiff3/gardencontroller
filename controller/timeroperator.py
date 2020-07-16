##############################################################
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International
# License.
#
# Author : Dominic Eschweiler

import time
import threading

class TimerOperator:
    def __init__(self, trigger_target, off_intervall, on_intervall):
        self.trigger_target = trigger_target
        self.off_intervall = off_intervall * 60
        self.on_intervall = on_intervall
        self.remaining_time = 0
        self.on = True
        self.active = True
        self.timer_thread = threading.Thread(target=self.timerThread, daemon=True)
        self.timer_thread.start()

    def __del__(self):
        self.active = False
        del self.trigger_target

    def timerThread(self):
        while self.active:
            self.trigger_target.on()
            self.on = True
            self.__sleep_counter(self.on_intervall)
            self.trigger_target.off()
            self.on = False
            self.__sleep_counter(self.off_intervall)

    def __sleep_counter(self, seconds):
        self.remaining_time = seconds
        while self.remaining_time >= 0:
            time.sleep(1)
            self.remaining_time -= 1
