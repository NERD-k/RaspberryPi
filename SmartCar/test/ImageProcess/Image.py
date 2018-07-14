#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from picamera import PiCamera
from PIL import Image
import time
import numpy
from collections import Counter
from L298NHBridge import HBridge
from datetime import datetime
    

def main():
    while True:
        try:
            Motors = HBridge(19, 26, 23, 24, 13, 21, 18)
            speed_run = 0
            angle_steer = 0
            #Motors.setMotorRun(0)
            #Motors.setMotorSteer(0)

            while True:
                all_start = time.time()
                with PiCamera() as camera:
                    stream = BytesIO()
                    for foo in camera.capture_continuous(stream, format='jpeg'):
                            # Truncate the stream to the current position (in case
                            # prior iterations output a longer image)
                            #PicStart = time.time()
                        stream.truncate()
                        stream.seek(0)
                            #if process(stream):
                                # 获取Image对象
                        image = Image.open(stream)
                                # RGB 通道分离
                        r, g, b = image.split()
            
                        arrayIm = numpy.array(r)
                        buff = numpy.where(arrayIm == arrayIm.max())
                        hang = Counter(buff[0])
                        lie = Counter(buff[1])
                        hang1 = max(hang.items(), key=lambda x: x[1])[0]
                        lie1 = max(lie.items(), key=lambda x: x[1])[0]
                        #PicStop = time.time()
                        #RunStart = time.time()
                        if hang1 < 700:
                            speedrun = 0.2
                        else:
                            speedrun = 0
                        anglesteer = 5 * (lie1 - 640) /640
                        #if lie1 < 640:
                        #    anglesteer = -2 * (640 - lie1)/640
                        #else:
                        #    anglesteer = 2 * (lie1 - 640)/640
                            
                        Motors.setMotorRun(speedrun)
                        Motors.setMotorSteer(anglesteer)
                        #if arrayIm.max() > 200:
                        #    Motors.setMotorRun(speedrun)
                        #    Motors.setMotorSteer(anglesteer)
                        #else:
                        #    Motors.setMotorRun(0)
                        #    Motors.setMotorSteer(0)
                        print(arrayIm.max(), hang1, lie1, speedrun, anglesteer)

                        stream.truncate()
                        stream.seek(0)
            
                all_end = time.time()
                print(all_end - all_start)
        except:
            Motors.exit()
            exit()

if __name__ == '__main__':
    main()
