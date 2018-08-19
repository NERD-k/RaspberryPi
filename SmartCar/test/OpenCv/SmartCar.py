#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:       孔NERD
# Email:        smallnerd.k@gmail.com
# Date:         2018-7-13

from multiprocessing import Process, Pipe
from io import BytesIO
from picamera import PiCamera
import picamera.array
import cv2
import time
import numpy
from collections import Counter

def func(p):
    with PiCamera() as camera:
        camera.resolution = (1280, 720)
        stream = BytesIO()
        for foo in camera.capture_continuous(stream, format='jpeg'):
                # Truncate the stream to the current position (in case
                # prior iterations output a longer image)
            #stream.truncate()
            #stream.seek(0)
            #if process(stream):
            #while True:
            #stream.truncate()
            #stream.seek(0)
            temp = time.time()
            print(temp)
                                # 获取Image对象
                #print(type(stream))
                
            image = cv2.imread(stream)
                                    # RGB 通道分离
            b, g, r = cv2.split(img) 
            arrayIm = numpy.array(r)
            buff = numpy.where(arrayIm == arrayIm.max())
            hang = Counter(buff[0])
            lie = Counter(buff[1])
            hang1 = max(hang.items(), key=lambda x: x[1])[0]
            lie1 = max(lie.items(), key=lambda x: x[1])[0]
                #PicStop = time.time()
                #RunStart = time.time()
            if hang1 < 700:
                speedrun = 0.05
            else:
                speedrun = 0
            anglesteer = 5 * (lie1 - 640) /640

            p.send([speedrun, anglesteer])
            p.send(image)
            print(time.time()-temp)
            stream.truncate()
            stream.seek(0)

def main():
    try:
        parent_side, child_side = Pipe()
        #print("Parent process start, %s" % time.ctime())
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
