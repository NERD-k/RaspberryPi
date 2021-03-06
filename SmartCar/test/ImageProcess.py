#!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import BytesIO
from picamera import PiCamera
from PIL import Image
import time
import numpy
from collections import Counter
from L298NHBridge import HBridge

class GetPosition(object):
    def __init__(self):
        pass

    def ProcessData(self):
        with PiCamera() as camera:
            stream = BytesIO()
            for foo in camera.capture_continuous(stream, format='jpeg'):
                stream.truncate()
                stream.seek(0)
                # Turn the stream(the memory flow) to image(Object)
                image = Image.open(stream)
                # Separate image channel, [red, green, bule]
                r, g, b = image.split()
                # turn the data of image to the array
                arrayIm = numpy.array(r)
                # find the position of red light
                buff = numpy.where(arrayIm == arrayIm.max())
                hang = Counter(buff[0])
                lie = Counter(buff[1])
                hang1 = max(hang.items(), key = lambda x: x[1])[0]
                lie1 = max(lie.items(), key = lambda x: x[1])[0]
                print(hang1, lie1, arrayIm.max())

                # Reset memory flow
                stream.truncate()
                stream.seek(0)

                # returm the distance and angle
                return(distance, angle)

