#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD
# Email:        smallnerd.k@gmail.com
# Date:         2018-7-13

from multiprocessing import Process, Pipe
from picamera import PiCamera
#import picamera.array
import time
import numpy
from collections import Counter
import cv2
from picamera.array import PiRGBArray

def func(p):
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))
        time.sleep(0.1)
        for frame in camera.capture_continuous(rawCapture, format='rgb'):
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)
            #stream.truncate()
            #stream.seek(0)
            temp = time.time()
            print(temp)
              
            image = frame.array
            #arrayIm = image
            #arrayIm = numpy.array(image)
            arrayR = image[:, :, 0]

            blurred = cv2.GaussianBlur(arrayR, (5, 5), 0)
            ret, binary = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
            _, contours, hierarchy = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            

            buff = numpy.where(arrayR == arrayR.max())
            hang = Counter(buff[0])
            lie = Counter(buff[1])
            hang1 = max(hang.items(), key=lambda x: x[1])[0]
            lie1 = max(lie.items(), key=lambda x: x[1])[0]
            if hang1 < 350:
                speedrun = 0.05
            else:
                speedrun = 0
            anglesteer = 5 * (lie1 - 320) / 320

            p.send([speedrun, anglesteer])
            #p.send(arrayR)
            print(time.time()-temp)
            rawCapture.truncate(0)

def main():
    try:
        parent_side, child_side = Pipe()
        p = Process(target=func, args=(child_side,))
        p.start()
        while True:
            #speedrun, anglesteer = parent_side.recv()
            #print(speedrun, "\t", anglesteer)
            print(parent_side.recv())
        #p.join()
        #temp = time.time()
        #if time.time() < temp+10:
        #    print(parent_side.recv())
        #    time.sleep(0.5)
        #else:
        #    parent_side.send(False)
        #    print("Parent process end, %s" % time.ctime())
        pass
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
