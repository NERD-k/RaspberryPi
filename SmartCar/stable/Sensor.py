#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD <smallnerd.k@gmail.com>
# Date:         2018-7-19

import RPi.GPIO as GPIO

class InfraredSensor(object):
    def __init__(self, sensor1_pin, sensor2_pin):
        GPIO.setmode(GPIO.BCM)

        self.sensor1_pin = sensor1_pin
        self.sensor2_pin = sensor2_pin

        self.SetupGPIO()
        
        GPIO.setwarnings(False)
        
    def SetupGPIO(self):
        GPIO.setup(self.sensor1_pin, GPIO.IN, pull_up_down=PUD_UP)
        GPIO.setup(self.sensor2_pin, GPIO.IN, pull_up_down=PUD_UP)
        
    def GetSignal1(self):
        if GPIO.input(self.sensor1_pin):
            signal1 = False
        else:
            signal1 = True
        return signal1

    def GetSignal2(self):
        if GPIO.input(self.sensor2_pin):
            signal2 = False
        else:
            signal2 = True
        return signal2

    def exit(self):
        GPIO.cleanup(self.sensor1_pin, self.sensor2_pin)
        
    
        
