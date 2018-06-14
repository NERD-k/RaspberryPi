#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")


class Car():
    def __init__(self, run_in1, run_in2, run_ena, steer_pwm):

    '''
    GPIO接口模式：BCM
    '''
    GPIO.setmode(GPIO.BCM)

    self.run_in1 = run_in1 
    self.run_in2 = run_in2 
    self.run_ena = run_ena 
    self.steer_pwm = steer_pwm 

    GPIO.setup(self.run_in1, GPIO.OUT)
    GPIO.setup(self.run_in2, GPIO.OUT)
    GPIO.setup(self.run_ena, GPIO.OUT)
    GPIO.setup(self.steer_pwm, GPIO.OUT)

    '''
    向前
    '''
    def forward(self):
        GPIO.output(self.run_in1, GPIO.HIGH)
        GPIO.output(self.run_in2, GPIO.LOW)
        self.p = GPIO.PWM(self.run_ena, ***)
        self.p.start(***)

    '''
    向后
    '''
    def backward(self):
        GPIO.output(self.run_in1, GPIO.LOW)
        GPIO.output(self.run_in2, GPIO.HIGH)
        self.p = GPIO.PWM(self.run_ena, ***)
        self.p.start(***)

    '''
    刹车
    '''
    def stop(self):
        GPIO.output(self.run_in1, GPIO.LOW)
        GPIO.output(self.run_in2, GPIO.LOW)
    
    '''
    悬空
    '''
    def stay(self):
        GPIO.output(self.run_in1, GPIO.HIGH)
        GPIO.output(self.run_in2, GPIO.HIGH)

    '''
    转向
    '''
    def steer(self):
        self.p = GPIO.PWM(self.steer_pwm, ***)
        self.p.start(***)

