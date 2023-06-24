#!/usr/bin/env python3
########################################################################
# Filename    : SteppingMotor.py
# Description : Drive SteppingMotor
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time 

# define pins connected to four phase ABCD of stepper motor
motorPins = (12, 16, 18, 22)
# define power supply order for rotating anticlockwise
CCWStep = (0x01,0x02,0x04,0x08)
# define power supply order for rotating clockwise
CWStep = (0x08,0x04,0x02,0x01)


def setup():
    GPIO.setmode(GPIO.BOARD) # use PHYSICAL GPIO Numbering
    for pin in motorPins:
        GPIO.setup(pin,GPIO.OUT)


def moveOnePeriod(direction,ms):
    """
    As for four phase stepping motor, four steps is a cycle.
    The function is used to drive the stepping motor clockwise or anticlockwise
    to take four steps.
    """
    for j in range(0,4,1): # cycle for power supply order
        for i in range(0,4,1): # assign to each pin
            if (direction == 1): # power supply order clockwise
                GPIO.output(motorPins[i],((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            else : # power supply order anticlockwise
                GPIO.output(motorPins[i],((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
        if(ms<3): # the delay can not be less than 3ms, otherwise it will exceed speed limit of the motor
            ms = 3
        time.sleep(ms*0.001)


# continuous rotation function, the parameter steps specifies the rotation cycles,
# every four steps is a cycle
def moveSteps(direction, ms, steps):
    for i in range(steps):
        moveOnePeriod(direction, ms)


# function used to stop motor
def motorStop():
    for i in range(0,4,1):
        GPIO.output(motorPins[i],GPIO.LOW)


def loop():
    while True:
        # rotating 360 deg clockwise, a total of 2048 steps in a circle, 512 cycles
        # moveSteps(1,3,512)
        moveSteps(1, 3, 128) # rotate 45 deg clockwise as requested
        # wait for one second
        time.sleep(1)
        # moveSteps(0,3,512) # rotating 360 deg anticlockwise
        moveSteps(1, 3, 128) # rotate 45 deg anti-clockwise as requested
        # wait for one second
        time.sleep(1)


def destroy():
    GPIO.cleanup() # Release resource


if __name__ == '__main__':
    # Program entrance
    print('Program is starting...')
    setup()
    try:
        loop()
    # Press ctrl-c to end the program.
    except KeyboardInterrupt:
        destroy()

