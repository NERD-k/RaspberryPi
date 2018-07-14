#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from picamera import PiCamera
from PIL import Image
import time
import numpy
from collections import Counter
from L298NHBridge import HBridge

    
while True:
    try:
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
                    # 对红色通道图像加强对比度
                    #enh_con = ImageEnhance.Contrast(r)  
                    #contrast = 2
                    #buff = enh_con.enhance(contrast)
                arrayIm = numpy.array(r)
                buff = numpy.where(arrayIm == arrayIm.max())
                hang = Counter(buff[0])
                lie = Counter(buff[1])
                hang1 = max(hang.items(), key=lambda x: x[1])[0]
                lie1 = max(lie.items(), key=lambda x: x[1])[0]
                #print(hang1, lie1, arrayIm.max())
                #PicStop = time.time()
                #RunStart = time.time()
                if hang1 < 700:
                    speedrun = 0.15
                else:
                    speedrun = 0
                if lie1 < 640:
                    anglesteer = -2 * (640 - lie1)/640
                else:
                    anglesteer = 2 * (lie1 - 640)/640
                    
                if arrayIm.max() > 200:
                    Motors.setMotorRun(speedrun)
                    Motors.setMotorSteer(anglesteer)
                else:
                    Motors.setMotorRun(0)
                    Motors.setMotorSteer(0)
                #print(speedrun)
                #RunStop = time.time()
                #print(PicStop - PicStart, RunStop - RunStart)
                stream.truncate()
                stream.seek(0)
    except:
        HBridge.exit(self)
