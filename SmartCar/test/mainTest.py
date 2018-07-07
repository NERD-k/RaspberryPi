#!/usr/bin/python3
# -*- coding -*-

# Arthor:       NERD
# Data:         2018-6-24
# Version:      1.0

from L298NHBridge import HBridge
from ImageProcess import ProcessData

def Init(self):
    Motors = HBridge(19, 26, 23, 24, 13, 21, 22)
    speed_run = 0
    angle_steer = 0

speed_run, angle_steer = ProcessImage()
Motors.setMotorRun(speed_run)
Motors.setMotorRun(angle_steer)

def main:
    Init(self)
    while True:
        try:
            pass
        expect RuntimeError:
            pass

if __name__ == "__main__":
    main()
