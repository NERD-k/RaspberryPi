#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD <smallnerd.k@gmail.com>
# Date:         2018-7-13

from multiprocessing import Process, Queue
from picamera import PiCamera
import time
from collections import Counter
import cv2
from picamera.array import PiRGBArray
from L298NHBridge import HBridge
from Sensor import InfraredSensor
from PIL import Image
import numpy

Motors = HBridge(19, 26, 23, 24, 13, 25, 5, 6)
Sensor = InfraredSensor(12, 16, 20, 21)

def funcImage(q):
   with PiCamera() as camera:
        camera.resolution = (960, 120)
        camera.framerate = 100
        rawCapture = PiRGBArray(camera, size=(960, 120))
        time.sleep(0.2)
        for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)

            time_image = time.time()
            image = frame.array

            array = image[:, :, 0]
            arrayR = numpy.array(array)
            MAX = arrayR.max()

            #arrayR[numpy.where(image[:, :, 1] > 210)] = 0
            #arrayR[numpy.where(image[:, :, 2] > 210)] = 0
            #blurred = cv2.GaussianBlur(arrayR, (32, 32), 0)
            ret, binary = cv2.threshold(arrayR, MAX-10, 255, cv2.THRESH_BINARY)
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

            #R, G, B = image[row, col, :]
            q.put([light, row, col, time_image])
            rawCapture.truncate(0)

def main():
    try:
        q = Queue()
        image = Process(target=funcImage, args=(q,))

        image.start()

        time.sleep(2)
        TIME = 0
        #list = [False, 0, 0]
        moderate, moderateFlag, stopCenter, stopLeft, stopRight = [False, False, False, False, False]

        while True:
            # 进程间通信，获取目标光源在图像中的信息
            #timeQueue = time.time()
            if q.empty():
                pass
            else:
                list = q.get()

            # 传感器
            if len(list) == 4:
                light, row, col, time_image = list
                if TIME != time_image:
                    print(time.time() - TIME)
                    TIME = time_image
            else:
                light, row, col = list
            #light, row, col = list
            moderate = Sensor.GetSignalLong()
            stopCenter = Sensor.GetSignalCenter()
            stopLeft = Sensor.GetSignalLeft()
            stopRight = Sensor.GetSignalRight()

            # 小车运动控制
            if light:
                angleSteer = 3 * (col - 480) / 480
                if row < 50:
                    speedRun = 0.03
                    moderateFlag = False
                elif not moderate:
                    speedRun = 0.03
                    moderateFlag = False
                #angleSteer = 3 * (col - 340) / 340
                elif moderateFlag:
                    speedRun = 0.0000001
                    Motors.setMotorRun(speedRun)
                    while stopCenter or stopLeft or stopRight:
                        speedRun = 0
                        Motors.setMotorRun(speedRun)
                        time.sleep(0.01)
                        speedRun = -0.1
                        Motors.setMotorRun(speedRun)
                        time.sleep(0.05)
                        speedRun = 0
                        Motors.setMotorRun(speedRun)

                        Motors.setArm(99)
                        time.sleep(0.7)
                        Motors.setArmBack(1)
                        time.sleep(0.5)
                        angleSteer = 0
                        Motors.setMotorSteer(angleSteer)
                        Motors.setMotorRun(-0.2)
                        time.sleep(0.3)
                        Motors.setMotorRun(0)
                        moderateFlag = False
                        stopCenter = False
                        stopLeft = False
                        stopRight = False
                    #else:
                    #    speedRun = 0.0000001
                else:
                    Motors.setMotorRun(0)
                    time.sleep(0.05)
                    Motors.setMotorRun(-0.4)
                    time.sleep(0.15)
                    speedRun = 0.0000001
                    moderateFlag = True 

                Motors.setMotorRun(speedRun)
                Motors.setMotorSteer(angleSteer)

            else:
                if moderate or stopCenter or stopLeft or stopRight:
                    speedRun = 0
                    angleSteer = 0
                    Motors.setMotorSteer(angleSteer)
                    Motors.setMotorRun(speedRun)
                    time.sleep(0.05)
                    #speedRun = -0.5
                    #angleSteer = 0
                    #Motors.setMotorSteer(angleSteer)
                    #Motors.setMotorRun(speedRun)
                    #time.sleep(0.2)
                    speedRun = -0.1
                    angleSteer = -5.5
                    Motors.setMotorSteer(angleSteer)
                    Motors.setMotorRun(speedRun)
                    time.sleep(0.2)
                    speedRun = 0
                    Motors.setMotorRun(speedRun)
                    time.sleep(0.05)
                    speedRun = 0.05
                    angleSteer = 5.5
                    Motors.setMotorSteer(angleSteer)
                    Motors.setMotorRun(speedRun)

                else:
                    speedRun = 0.05
                    angleSteer = 5.5
                    Motors.setMotorSteer(angleSteer)
                    Motors.setMotorRun(speedRun)
                #time.sleep(0.5)

            #print(speedRun, angleSteer, moderate, moderateFlag, stop)
            print(*list, moderate, moderateFlag, stopCenter, stopLeft, stopRight)
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
        Sensor.exit()
        pass

if __name__ == "__main__":
    main()
