#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Autor:        孔NERD
# Date:         2018-6-22
# VersGPIOn:      1.0
#Thanks for origin Autor's Ingmar Stape and kevin

# This module is designed to control two motors with a L298N H-Bridge

# Use this module by creating an instance of the class. To do so call the Init functGPIOn, then command as desired, e.g.
# import L298NHBridge
# HBridge = L298NHBridge.L298NHBridge()
# HBridge.Init()

# Import the libraries the class needs
import RPi.GPIO as GPIO
import time

class HBridge(object):

    def __init__(self, motor1_pin1, motor1_pin2, motor2_pin1, motor2_pin2, motor1pwm_pin,
            motor2pwm_pin, steerpwm_pin, armpwm_pin):
        GPIO.setmode(GPIO.BCM)
        # Constant values
        self.PWM_MAX = 100
        self.LEFT_MAX = 6.2
        self.RIGHT_MAX = 20.2
        self.CENTER = 13.2
        # Here we configure the GPGPIO settings for the left and right motors spinning directGPIOn.
        # It defines the four GPGPIO pins used as input on the L298 H-Bridge to set the motor mode (forward, reverse and stopp).
        self.motor1_in1_pin = motor1_pin1
        self.motor1_in2_pin = motor1_pin2
        self.motor2_in1_pin = motor2_pin1
        self.motor2_in2_pin = motor2_pin2
        self.motor1pwm_pin = motor1pwm_pin
        self.motor2pwm_pin = motor2pwm_pin
        self.steerpwm_pin = steerpwm_pin
        self.armpwm_pin = armpwm_pin
        self.SetupGPIO()
        self.motor1pwm = GPIO.PWM(self.motor1pwm_pin, 1000)
        self.motor2pwm = GPIO.PWM(self.motor2pwm_pin, 1000)
        self.steerpwm = GPIO.PWM(self.steerpwm_pin, 100)
        self.armpwm = GPIO.PWM(self.armpwm_pin, 330)
        self.InitPWM()
        # Disable warning from GPIO
        GPIO.setwarnings(False)

    def SetupGPIO(self):
        GPIO.setup(self.motor2_in1_pin, GPIO.OUT)
        GPIO.setup(self.motor2_in2_pin, GPIO.OUT)
        GPIO.setup(self.motor1_in1_pin, GPIO.OUT)
        GPIO.setup(self.motor1_in2_pin, GPIO.OUT)
        GPIO.setup(self.motor1pwm_pin, GPIO.OUT)
        GPIO.setup(self.motor2pwm_pin, GPIO.OUT)
        GPIO.setup(self.steerpwm_pin, GPIO.OUT)
        GPIO.setup(self.armpwm_pin, GPIO.OUT)

    def InitPWM(self):
        # Here we configure the GPGPIO settings for the left and right motors spinning speed.
        # It defines the two GPGPIO pins used as input on the L298 H-Bridge to set the motor speed with a PWM signal.
        self.motor1pwm.start(0)
        self.motor1pwm.ChangeDutyCycle(0)
        self.motor2pwm.start(0)
        self.motor2pwm.ChangeDutyCycle(0)
        self.steerpwm.start(0)
        #self.steerpwm.ChangeDutyCycle(0)
        self.armpwm.start(0)
        self.armpwm.ChangeDutyCycle(0)

    def resetMotorGPIO(self):
        GPIO.output(self.motor1_in1_pin, False)
        GPIO.output(self.motor1_in2_pin, False)
        GPIO.output(self.motor2_in1_pin, False)
        GPIO.output(self.motor2_in2_pin, False)

# setMotorMode()

# Sets the mode for the L298 H-Bridge which motor is in which mode.

# This is a short explanatGPIOn for a better understanding:
# motor         -> which motor is selected left motor or right motor
# mode          -> mode explains what actGPIOn should be performed by the H-Bridge

# setMotorMode(motor1, reverse)      -> The left motor is called by a functGPIOn and set into reverse mode
# setMotorMode(motor2, stopp)       -> The right motor is called by a functGPIOn and set into stopp mode
    def setMotorMode(self, motor, mode):

        if motor == "motor1":
            if mode == "reverse":
                GPIO.output(self.motor1_in1_pin, True)
                GPIO.output(self.motor1_in2_pin, False)
            elif  mode == "forward":
                GPIO.output(self.motor1_in1_pin, False)
                GPIO.output(self.motor1_in2_pin, True)
            else:
                GPIO.output(self.motor1_in1_pin, False)
                GPIO.output(self.motor1_in2_pin, False)

        elif motor == "motor2":
            if mode == "reverse":
                GPIO.output(self.motor2_in1_pin, False)
                GPIO.output(self.motor2_in2_pin, True)
            elif  mode == "forward":
                GPIO.output(self.motor2_in1_pin, True)
                GPIO.output(self.motor2_in2_pin, False)
            else:
                GPIO.output(self.motor2_in1_pin, False)
                GPIO.output(self.motor2_in2_pin, False)
        else:
            self.resetMotorGPGPIO()

# SetMotorLeft(power)

# Sets the drive level for the left motor, from +1 (max) to -1 (min).

# This is a short explanatGPIOn for a better understanding:
# SetMotorLeft(0)     -> left motor is stopped
# SetMotorLeft(0.75)  -> left motor moving forward at 75% power
# SetMotorLeft(-0.5)  -> left motor moving reverse at 50% power
# SetMotorLeft(1)     -> left motor moving forward at 100% power
    def setMotorRun(self, power):
        if power < 0:
            # Reverse mode for the left motor
            self.setMotorMode("motor1", "reverse")
            pwm = -self.PWM_MAX * power
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        elif power > 0:
            # Forward mode for the left motor
            self.setMotorMode("motor1", "forward")
            pwm = self.PWM_MAX * power
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
                print(pwm)
        else:
            # Stopp mode for the left motor
            self.setMotorMode("motor1", "stopp")
            pwm = 0
#       print "SetMotorLeft", pwm
        self.motor1pwm.ChangeDutyCycle(pwm)

# SetMotorRight(power)

# Sets the drive level for the right motor, from +1 (max) to -1 (min).

# This is a short explanatGPIOn for a better understanding:
# SetMotorRight(0)     -> right motor is stopped
# SetMotorRight(0.75)  -> right motor moving forward at 75% power
# SetMotorRight(-0.5)  -> right motor moving reverse at 50% power
# SetMotorRight(1)     -> right motor moving forward at 100% power
    def setMotorRun2(self, power):
        if power < 0:
            # Reverse mode for the right motor
            self.setMotorMode("motor2", "reverse")
            pwm = -self.PWM_MAX * power
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        elif power > 0:
            # Forward mode for the right motor
            self.setMotorMode("motor2", "forward")
            pwm = self.PWM_MAX * power
            if pwm > self.PWM_MAX:
                pwm = self.PWM_MAX
        else:
            # Stopp mode for the right motor
            self.setMotorMode("motor2", "stopp")
            pwm = 0
        #print "SetMotorRight", pwm
        self.motor2pwm.ChangeDutyCycle(pwm)

    def setMotorSteer(self, power):
        if power < 0:
            pwm = power + self.CENTER
            if pwm < self.LEFT_MAX:
                pwm = self.LEFT_MAX
        elif power > 0:
            pwm = power + self.CENTER
            if pwm > self.RIGHT_MAX:
                pwm = self.RIGHT_MAX
        else:
            pwm = self.CENTER
        self.steerpwm.ChangeDutyCycle(pwm)

    def setArm(self, power):
        pwm = power
        self.armpwm.ChangeDutyCycle(pwm)

    def setArmBack(self, power):
        pwm = power
        self.armpwm.ChangeDutyCycle(pwm)

# Program will clean up all GPGPIO settings and terminates
    def exit(self):
        self.resetMotorGPIO()
        GPIO.cleanup()

