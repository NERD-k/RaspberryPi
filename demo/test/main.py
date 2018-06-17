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


def main():
    while True:
        try:

        except RuntimeError:
            print("It's exist error! Check the code."
if __name__ == '__main__':
    main()
