#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:           孔NERD
# Date:             2018-8-3

import RPi.GPIO as GPIO

class SteeringGear():

    def __init__(self, steer1pwm_pin, steer2pwm_pin):
        GPIO.setmode(GPIO.BCM)

        self.steerPwm_pin = steer1pwm_pin
        self.armPwm_pin = steer2pwm_pin

        self.SetupGPIO()
        self.steerPwm = GPIO.PWM(self.steerPwm_pin, 200)
        self.armPwm = GPIO.PWM(self.armPwm_pin, 200)

        self.InitPWM()

        GPIO.setwarnings(False)

    def SetupGPIO(self):
        GPIO.setup(self.steerPwm_pin, GPIO.OUT)
        GPIO.setup(self.armPwm_pin, GPIO.OUT)

    def InitPWM(self):
        self.steerPwm.start(0)
        self.steerPwm.ChangeDutyCycle(0)
        self.armPwm.start(0)
        self.armPwm.ChangeDutyCycle(0)

    def Steer(self, angle):
        pass

    def Arm(self, angle):
        pass

    def exit(self):
        GPIO.cleanup(self.steerPwm_pin, self.armPwm_pin)
