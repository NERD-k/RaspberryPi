#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD <smallnerd.k@gmail.com>
# Date:         2018-7-19

import RPi.GPIO as GPIO
import time

class InfraredSensor(object):
    def __init__(self, sensorLong_pin, sensorCenter_pin, sensorLeft_pin, sensorRight_pin):
        GPIO.setmode(GPIO.BCM)

        self.sensorLong_pin = sensorLong_pin
        self.sensorCenter_pin = sensorCenter_pin
        self.sensorLeft_pin = sensorLeft_pin
        self.sensorRight_pin = sensorRight_pin

        self.SetupGPIO()
        
        GPIO.setwarnings(False)
        
    def SetupGPIO(self):
        GPIO.setup(self.sensorLong_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sensorCenter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sensorLeft_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sensorRight_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def GetSignalLong(self):
        if GPIO.input(self.sensorLong_pin):
            signalLong = True
        else:
            signalLong = False
        return signalLong

    def GetSignalCenter(self):
        if GPIO.input(self.sensorCenter_pin):
            signalCenter = False
        else:
            signalCenter = True
        return signalCenter

    def GetSignalLeft(self):
        if GPIO.input(self.sensorLeft_pin):
            signalLeft = False
        else:
            signalLeft = True
        return signalLeft

    def GetSignalRight(self):
        if GPIO.input(self.sensorRight_pin):
            signalRight = False
        else:
            signalRight = True
        return signalRight

    def exit(self):
        GPIO.cleanup(self.sensorLong_pin, self.sensorCenter_pin, self.sensorLeft_pin, self.sensorRight_pin)
 
