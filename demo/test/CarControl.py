#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")

'''
小车硬件控制
'''
class Car():
    def __init__(self, run_in1, run_in2, run_ena, steer_pwm):
        '''
        Car doc
        '''

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.run_in1, GPIO.OUT)
        GPIO.setup(self.run_in2, GPIO.OUT)
        GPIO.setup(self.run_ena, GPIO.OUT)
        GPIO.setup(self.steer_pwm, GPIO.OUT)

    def getAPI(self):
        pass

    def setAPI(self, run_in1, run_in2, run_ena, steer_pwm):
        self.run_in1 = run_in1
        self.run_in2 = run_in2
        self.run_ena = run_ena
        self.steer_pwm = steer_pwm

    def setFreq(self, run_freq, turn_freq):
        self.run_freq = run_freq
        self.turn_freq = turn_freq

    '''
    向前
    '''
    def forward(self, speed):
        GPIO.output(self.run_in1, GPIO.HIGH)
        GPIO.output(self.run_in2, GPIO.LOW)
        if !exist(self.run):
            self.run = GPIO.PWM(self.run_ena, run_freq)
            self.run.start(speed)
        else:
            self.run.stop()
            self.run.start(speed)

    '''
    向后
    '''
    def backward(self, speed):
        GPIO.output(self.run_in1, GPIO.LOW)
        GPIO.output(self.run_in2, GPIO.HIGH)
        self.back = GPIO.PWM(self.run_ena, run_freq)
        self.back.start(speed)

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
    def steer(self, angle):
        if !exist(self.turn):
            self.turn = GPIO.PWM(self.steer_pwm, self.turn_freq)
            self.turn.start(angle)
        else:
            self.turn.stop()
            self.turn.start(angle)

    '''
    清除GPIO的模式
    '''
    def cleanup(self):
        if exist(self.run):
            self.run.stop()
        if exist(self.turn):
            self.turn.stop()
        GPIO.cleanup()


'''
小车软件驱动
'''
class CarMove():
    '''
    CarMove doc
    '''
    def __init__(self, speed, angle):
        self._speed = speed
        self._angle = angle

    def move(self):
        if self._speed > 0:
            forward(self._speed)
        elif speed < 0:
            self._speed = abs(self._speed)
            backward(self._speed)
        else:
            stay()

    def turn(self):
        steer(self._angle)

