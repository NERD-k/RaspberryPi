#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Autor:        孔NERD
# Date:         2018-6-22
# Version:      1.0
#Thanks for origin Autor's Ingmar Stape and kevin

# This module is designed to control two motors with a L298N H-Bridge

# Use this module by creating an instance of the class. To do so call the Init function, then command as desired, e.g.
# import L298NHBridge
# HBridge = L298NHBridge.L298NHBridge()
# HBridge.Init()

# Import the libraries the class needs
import RPi.GPIO as io
import time

class HBridge(object):

    def __init__(self, motor1_pin1, motor1_pin2, motor2_pin1, motor2_pin2, motor1pwm_pin, motor2pwm_pin):
        io.setmode(io.BCM)
        # Constant values
        self.PWM_MAX = 100
        # Here we configure the GPIO settings for the left and right motors spinning direction.
        # It defines the four GPIO pins used as input on the L298 H-Bridge to set the motor mode (forward, reverse and stopp).
        self.motor1_in1_pin = motor1_pin1
        self.motor1_in2_pin = motor1_pin2
        self.motor2_in1_pin = motor2_pin1
        self.motor2_in2_pin = motor2_pin2
        self.motor1pwm_pin = motor1pwm_pin
        self.motor2pwm_pin = motor2pwm_pin
        self.SetupGPIO()
        self.motor1pwm = io.PWM(self.motor1pwm_pin,100)
        self.motor2pwm = io.PWM(self.motor2pwm_pin,100)
        self.InitPWM()
        # Disable warning from GPIO
        io.setwarnings(False)

    def SetupGPIO(self):
        io.setup(self.motor2_in1_pin, io.OUT)
        io.setup(self.motor2_in2_pin, io.OUT)
        io.setup(self.motor1_in1_pin, io.OUT)
        io.setup(self.motor1_in2_pin, io.OUT)
        io.setup(self.motor1pwm_pin, io.OUT)
        io.setup(self.motor2pwm_pin, io.OUT)

    def InitPWM(self):
        # Here we configure the GPIO settings for the left and right motors spinning speed.
        # It defines the two GPIO pins used as input on the L298 H-Bridge to set the motor speed with a PWM signal.
        self.motor1pwm.start(0)
        self.motor1pwm.ChangeDutyCycle(0)
        self.motor2pwm.start(0)
        self.motor2pwm.ChangeDutyCycle(0)

    def resetMotorGPIO(self):
        io.output(self.motor1_in1_pin, False)
        io.output(self.motor1_in2_pin, False)
        io.output(self.motor2_in1_pin, False)
        io.output(self.motor2_in2_pin, False)

# setMotorMode()

# Sets the mode for the L298 H-Bridge which motor is in which mode.

# This is a short explanation for a better understanding:
# motor         -> which motor is selected left motor or right motor
# mode          -> mode explains what action should be performed by the H-Bridge

# setMotorMode(motor1, reverse)      -> The left motor is called by a function and set into reverse mode
# setMotorMode(motor2, stopp)       -> The right motor is called by a function and set into stopp mode
    def setMotorMode(self, motor, mode):

        if motor == "motor1":
            if mode == "reverse":
                io.output(self.motor1_in1_pin, True)
                io.output(self.motor1_in2_pin, False)
            elif  mode == "forward":
                io.output(self.motor1_in1_pin, False)
                io.output(self.motor1_in2_pin, True)
            else:
                io.output(self.motor1_in1_pin, False)
                io.output(self.motor1_in2_pin, False)

        elif motor == "motor2":
            if mode == "reverse":
                io.output(self.motor2_in1_pin, False)
                io.output(self.motor2_in2_pin, True)
            elif  mode == "forward":
                io.output(self.motor2_in1_pin, True)
                io.output(self.motor2_in2_pin, False)
            else:
                io.output(self.motor2_in1_pin, False)
                io.output(self.motor2_in2_pin, False)
        else:
            self.resetMotorGPIO()

# SetMotorLeft(power)

# Sets the drive level for the left motor, from +1 (max) to -1 (min).

# This is a short explanation for a better understanding:
# SetMotorLeft(0)     -> left motor is stopped
# SetMotorLeft(0.75)  -> left motor moving forward at 75% power
# SetMotorLeft(-0.5)  -> left motor moving reverse at 50% power
# SetMotorLeft(1)     -> left motor moving forward at 100% power
    def setMotorLeft(self, power):
        if power < 0:
            # Reverse mode for the left motor
            self.setMotorMode("motor1", "reverse")
            pwm = -int(self.PWM_MAX * power)
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        elif power > 0:
            # Forward mode for the left motor
            self.setMotorMode("motor1", "forward")
            pwm = int(self.PWM_MAX * power)
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        else:
            # Stopp mode for the left motor
            self.setMotorMode("motor1", "stopp")
            pwm = 0
#       print "SetMotorLeft", pwm
        self.motor1pwm.ChangeDutyCycle(pwm)

# SetMotorRight(power)

# Sets the drive level for the right motor, from +1 (max) to -1 (min).

# This is a short explanation for a better understanding:
# SetMotorRight(0)     -> right motor is stopped
# SetMotorRight(0.75)  -> right motor moving forward at 75% power
# SetMotorRight(-0.5)  -> right motor moving reverse at 50% power
# SetMotorRight(1)     -> right motor moving forward at 100% power
    def setMotorRight(self, power):
        if power < 0:
            # Reverse mode for the right motor
            self.setMotorMode("motor2", "reverse")
            pwm = -int(self.PWM_MAX * power)
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        elif power > 0:
            # Forward mode for the right motor
            self.setMotorMode("motor2", "forward")
            pwm = int(self.PWM_MAX * power)
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        else:
            # Stopp mode for the right motor
            self.setMotorMode("motor2", "stopp")
            pwm = 0
        #print "SetMotorRight", pwm
        self.motor2pwm.ChangeDutyCycle(pwm)

# Program will clean up all GPIO settings and terminates
    def exit(self):
        self.resetMotorGPIO()
        io.cleanup()

