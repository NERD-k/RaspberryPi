#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Author:       孔NERD
# Email:        smallnerd.k@gmail.com
# Date:         2018-7-5

from io import BytesIO
from picamera import PiCamera
from PIL import Image
import time
from L298NHBridge import HBridge

IS_TEST = True
DEBUG = False

if IS_TEST:
    DEBUG = True
    LOG_PATH = '/home/pi/smartcar.log'

def log(*args, **kwargs):
    s = ' '.join(args)
    if 'pkt' in kwargs and DEBUG == True:
        s += '\n\tinfo: ' + kwargs['pkt']
    s += ''
    print(s)
    if DEBUG:
        with open(LOG_PATH, 'a') as f:
            try:
                f.write(s)
                f.write('\n')
            except:
                f.write('log failed.' + '\n')

def Init():
    Motors = HBridge(19, 26, 23, 24, 13, 21, 22)
    speed_run = 0
    angle_steer = 0


def Image():
    with PiCamera() as camera:
        stream = BytesIO()
        camera.capture_continuous(stream, format='png')
        stream.truncate()
        strea.seek(0)

        image = Image.open(stream)
        r, g, b = image.spilt()
        r.save('/home/pi/Image/Image{counter}')
 
        stream.truncate()
        stream.seek(0)

def main():
    Init()
    while True:
        try:
            Image()
            Motors.setMotorRun(20)
        except RuntimeError:
            print("Error, out of main loop!")

        #log('speed: ' + speed_run)
        #log('Image: ' + {counter})

if __name__ == '__main__':
    main()

