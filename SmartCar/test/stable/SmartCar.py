#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD <smallnerd.k@gmail.com>
# Date:         2018-7-13

from multiprocessing import Process, Pipe, Queue
from picamera import PiCamera
import time
#import numpy
from collections import Counter
import cv2
from picamera.array import PiRGBArray
from L298NHBridge import HBridge
from Sensor import InfraredSensor

Motors = HBridge(19, 26, 23, 24, 13, 21, 18, 25)
Sensor = InfraredSensor(17, 27)

def funcImage(q):
   with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        time.sleep(0.2)
        for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)
 
            image = frame.array

            arrayR = image[:, :, 0]

            blurred = cv2.GaussianBlur(arrayR, (5, 5), 0)
            ret, binary = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
            _, contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            col = 0
            row = 0
            if len(contours) > 0:
                light = True
                cnts = contours[0]
                #hull = cv2.convexHull(points, hull, clockwise, returnPoints)
                hull = cv2.convexHull(cnts)
                (x, y), radius = cv2.minEnclosingCircle(cnts)
                col, row = (int(x), int(y))
            else:
                light = False

            q.put([light, row, col])
            rawCapture.truncate(0)
            #print("all:", time.time()-Temp)

def main():
    try:
        q = Queue()
        image = Process(target=funcImage, args=(q,))

        image.start()

        list = [False, 0, 0]
        moderate, moderateFlag, stop = [False, False, False]

        while True:
            # 进程间通信，获取目标光源在图像中的信息
            #timeQueue = time.time()
            if q.empty():
                pass
            else:
                list = q.get()

            # 传感器
            moderate = Sensor.GetSignal1()
            stop = Sensor.GetSignal2()
            
            # 小车运动控制
            if light:
                angleSteer = 3 * (col - 340) / 340
                if row < 350:
                    speedRun = 0.05
                elif not moderate:
                    speedRun = 0.05
                #angleSteer = 3 * (col - 340) / 340
                elif moderateFlag:
                    if stop:
                        speedRun = 0
                        Motors.setMotorRun(speedRun)
                        Motors.setArm(45)
                        time.sleep(0.7)
                        Motors.setArmBack(1)
                        time.sleep(0.5)
                        angleSteer = 0
                        Motors.setMotorSteer(angleSteer)
                        Motors.setMotorRun(-0.2)
                        time.sleep(0.1)
                        Motors.setMotorRun(0)
                        moderateFlag = False
                    else:
                        speedRun = 0.01
                        pass
                else:
                    Motors.setMotorRun(0)
                    time.sleep(0.1)
                    Motors.setMotorRun(-0.2)
                    time.sleep(0.05)
                    speedRun = 0.02
                    moderateFlag = True 

                Motors.setMotorRun(speedRun)
                Motors.setMotorSteer(angleSteer)

            else:
                speedRun = 0.01
                angleSteer = -5.5
                Motors.setMotorSteer(angleSteer)
                Motors.setMotorRun(speedRun)
                #time.sleep(0.5)

            #print(speedRun, angleSteer, moderate, moderateFlag, stop)
            print(*list, moderate, moderateFlag, stop)
            #print("All: ", time.time() - timeQueue, "\tImage: ",timePipe - timeQueue, "\tPipe: ",
            #        timeControl - timePipe, "\tControl: ", time.time() - timeControl)
        #if time.time() < temp+10:
        #    print(parent_side.recv())
        #    time.sleep(0.5)
        #else:
        #    parent_side.send(False)
        #    print("Parent process end, %s" % time.ctime())
        pass
    except KeyboardInterrupt:
        Motors.exit()
        pass

if __name__ == "__main__":
    main()
