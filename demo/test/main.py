#!/usr/bin/python3
# -*- coding: utf-8 -*-

import CarControl
from picamera import PiCamera
from time import sleep

def getPhoto():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/picture.jpg')
    camera.stop_preview()


'''
小车状态监控
'''
def carStatus():
    pass


def main():
    '''
    小车硬件接口设置
    '''
    Car.setAPI(11, 12, 13, 14)

    while True:
        try:
            CarControl.CarMove(2)
            sleep(50)
            CarControl.CarMove(0)
            sleep(50)
            CarControl.CarMove(-1)
            sleep(50)
        except RuntimeError:
            print("It's exist bug! Plese check the code."
if __name__ == '__main__':
    main()
