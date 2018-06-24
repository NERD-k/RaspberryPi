#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from picamera import PiCamera
from PIL import Image
import time
import numpy
from collections import Counter

with PiCamera() as camera:
    stream = BytesIO()
    for foo in camera.capture_continuous(stream, format='png'):
        # Truncate the stream to the current position (in case
        # prior iterations output a longer image)
        stream.truncate()
        stream.seek(0)
        if process(stream):
            # 获取Image对象
            image = Image.open(steam)
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
            lie1 = max(lie.iterms(), key=lambda x: x[1])[0]
            if hang1 < 700:
                pass
            else:
                pass
            if lie1 < 640:
                pass
            else:
                pass

