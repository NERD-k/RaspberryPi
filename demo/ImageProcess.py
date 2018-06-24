#!/usr/bin/python3
# -*- coding: utf-8 -*-

from picamera import PiCamera
from time import sleep
from PIL import Image 

camera = PiCamera()
camera.start_preview()
