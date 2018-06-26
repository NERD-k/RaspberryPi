#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Autor:    Ingmar Stapel
# Date:     20141229
# Version:  1.0
# Homepage: www.raspberry-pi-car.com

import sys, tty, termios, os
from L298NHBridge import HBridge

speedrun = 0
anglesteer = 0

Motors = HBridge(19, 26, 23, 24, 13, 21, 22)
# Instructions for when the user has an interface
print("w/s: direction")
print("a/d: steering")
print("q: stops the motors")
print("p: print motor speed (L/R)")
print("x: exit")

# The catch method can determine which key has been pressed
# by the user on the keyboard.
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Infinite loop
# The loop will not end until the user presses the
# exit key 'X' or the program crashes...

def printscreen():
    # Print the motor speed just for interest
    os.system('clear')
    print("w/s: direction")
    print("a/d: steering")
    print("q: stops the motors")
    print("x: exit")
    print("========== Speed Control ==========")
    print("run motor:  ", speedrun)
    print("steer motor: ", anglesteer)

while True:
    # Keyboard character retrieval method. This method will save
    # the pressed key into the variable char
    char = getch()



    # The car will drive forward when the "w" key is pressed
    if(char == "w"):

        # accelerate the RaPi car
        speedrun = speedrun + 0.1

        if speedrun > 1:
            speedrun = 1

        Motors.setMotorRun(speedrun)
        #Motors.setMotorSteer(anglesteer)
        printscreen()

    # The car will reverse when the "s" key is pressed
    if(char == "s"):

        # slow down the RaPi car
        speedrun = speedrun - 0.1

        if speedrun < -1:
            speedrun = -1

        Motors.setMotorRun(speedrun)
        #Motors.setMotorSteer(anglesteer)
        printscreen()

    # Stop the motors
    if(char == "q"):
        speedrun = 0
        speedsteer = 0
        Motors.setMotorRun(speedrun)
        Motors.setMotorSteer(anglesteer)
        printscreen()

    # The "d" key will toggle the steering steer
    if(char == "d"):
        anglesteer = anglesteer + 0.5

        if anglesteer > 5.5:
            anglesteer = 5.5


        #Motors.setMotorRun(speedrun)
        Motors.setMotorSteer(anglesteer)
        printscreen()

    # The "a" key will toggle the steering run
    if(char == "a"):
        anglesteer = anglesteer - 0.5

        if anglesteer < -5.5:
            anglesteer = -5.5

        #Motors.setMotorRun(speedrun)
        Motors.setMotorSteer(anglesteer)
        printscreen()

    # The "x" key will break the loop and exit the program
    if(char == "x"):
        Motors.setMotorRun(0)
        Motors.setMotorSteer(0)
        Motors.exit()
        print("Program Ended")
        break

    # The keyboard character variable char has to be set blank. We need
    # to set it blank to save the next key pressed by the user
    char = ""
# End
