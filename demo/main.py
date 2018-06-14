#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(40, GPIO.OUT)

p = GPIO.PWM(40, 300)
p.start(50)
input('Press return to stop:')
p.stop()
GPIO.cleanup()



