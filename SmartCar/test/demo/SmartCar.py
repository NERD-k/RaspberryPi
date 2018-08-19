#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD <smallnerd.k@gmail.com>
# Date:         2018-7-13

from multiprocessing import Process, Pipe, Queue
from picamera import PiCamera
#import picamera.array
import serial
import time
#import numpy
from collections import Counter
import cv2
from picamera.array import PiRGBArray
from L298NHBridge import HBridge

Motors = HBridge(19, 26, 23, 24, 13, 21, 18, 25)

def carControl(light, row, col, distance):
    flag = False
    if light:
        angleSteer = 3 * (col - 340) / 340
        if row < 350:
            speedRun = 0.05
        elif distance > 50:
            speedRun = 0.05
            pass
            #angleSteer = 3 * (col - 340) / 340
        elif flag:
            speedRun = 0.02
            if distance < 10:
                speedRun = 0
                Motors.setMotorRun(speedRun)
                Motors.setArm(45)
                time.sleep(0.7)
                Motors.setArmBack(1)
                time.sleep(0.5)
                angleSteer = 0
                Motors.setMotorSteer(angleSteer)
                Motors.setMotorRun(0.2)
                time.sleep(0.1)
                Motors.setMotorRun(0)
            else:
                pass
        else:
            Motors.setMotorRun(0)
            time.sleep(0.1)
            Motors.setMotorRun(-0.2)
            time.sleep(0.05)
            speedRun = 0.02
            flag = True 

        Motors.setMotorRun(speedRun)
        Motors.setMotorSteer(angleSteer)

    else:
        speedRun = -0.05
        angleSteer = -5.5
        Motors.setMotorSteer(angleSteer)
        Motors.setMotorRun(speedRun)
        #time.sleep(0.5)

    #print(speedRun, angleSteer)

def funcSensor(child_side):
    ser = serial.Serial("/dev/ttyACM0", 115200)
    temp = 0
    while True:
        try:
            count = ser.inWaiting()
            if count >= 8:
                recvData = ser.read(count)
                recv = max(Counter(recvData).items(), key=lambda x: x[1])[0]
                temp = recv
            else:
                recv = temp
            ser.flushInput()
            child_side.send(int(recv))
        except KeyboardInterrupt:
            if ser != None:
                ser.close()
            else:
                ser.close()
                pass


def funcImage(q):
   with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        #print(time.time())
        time.sleep(0.2)
        for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)
            #print(time.time())
            Temp = time.time()
 
            image = frame.array
            #arrayIm = image
            #arrayIm = numpy.array(image)
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

            #buff = numpy.where(arrayR == arrayR.max())
            #hang = Counter(buff[0])
            #lie = Counter(buff[1])
            #hang1 = max(hang.items(), key=lambda x: x[1])[0]
            #lie1 = max(lie.items(), key=lambda x: x[1])[0]
            #if hang1 < 350:
            #    speedrun = 0.05
            #else:
            #    speedrun = 0
            #anglesteer = 3 * (lie1 - 240) / 240
            
            #speedRun = 0.05
            #angleSteer = 3 * (lie - 240) / 240

            q.put([light, row, col])
            #p.send(time.time())
            #p.send([light, row, col])
            #print(lignt, row, col)
            #p.send(arrayR)
            rawCapture.truncate(0)
            #print("all:", time.time()-Temp)

def main():
    try:
        q = Queue()
        parent_side, child_side = Pipe()
        image = Process(target=funcImage, args=(q,))
        sensor = Process(target=funcSensor, args=(child_side,))

        image.start()
        sensor.start()

        list = [False, 0, 0]
        distance = 0
        while True:
            #timeQueue = time.time()
            if q.empty():
                pass
            else:
                list = q.get()
            #timePipe = time.time()
            distance = parent_side.recv()
            #list = parent_side.recv()
            #child_time = parent_side.recv()
            #print("before:", temp - child_time)
            #print(time.time() - child_time)
            #print("Wait: ", time.time() - temp)
            #timeControl = time.time()
            carControl(*list, distance)
            print(list, distance)
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
