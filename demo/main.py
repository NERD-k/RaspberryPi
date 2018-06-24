#!/usr/bin/python3
# -*- coding: utf-8 -*-

import L298NHBridge


clsss SmartCar(object):
    def __init__(self, motors):
        self.motors = motors
        self.speed = 0
        self.arrow = "forward"
        self.status = False

    def SmartCarAction(self):
        pass

    def SmartCarForward(self):
        # print("The car forward move.")
        pass

    def SmartCarBack(self):
        # print("The car back move.")
        pass

    def SmartCarStop(self):
        # print("The car stop.")
        pass

    def SmartCarRight(self):
        # print("The car turn right.")
        pass

    def SmartCarLeft(self):
        # print("The car turn left.")
        pass



def main():
    while True:
        try:

        except RuntimeError:
            print("It's exist error! Check the code.")
if __name__ == '__main__':
    main()
