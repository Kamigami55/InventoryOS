#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
InventoryOS camera main.py
==============

Main script of InventoryOS camera component

Before run this script, you should set credential
set environment variable $GOOGLE_APPLICATION_CREDENTIALS
to the path of your credential.json downloaded from
google cloud
'''


from __future__ import print_function
from enum import Enum
import io
import os
from imutils.video import VideoStream
import RPi.GPIO as GPIO
import signal
import time
import threading

from packages.InventoryOSApp import InventoryOSApp


class ModeType(Enum):
    BORROW = 1
    RETURN = 2

mode = ModeType.BORROW

window = None
windowHasCleanedUp = False


def cleanup():
    global window
    global windowHasCleanedUp

    if not windowHasCleanedUp:
        print("Stopping window loop")
        window.cleanup()

    GPIO.cleanup()
    print("GPIO successfully cleaned up")
    print("Program exit")
    exit(0)


def main():

    global window
    global windowHasCleanedUp

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
            '/home/eason/projects/InventoryOS/InventoryOS-camera/google-vision-credential.json'

    GPIO.setwarnings(False)


    print("[INFO] warming up camera...")
    vs = VideoStream().start()
    time.sleep(1.0)

    # start the app
    window = InventoryOSApp(vs)
    window.root.mainloop()

    # Window exited
    print("Window close button pressed (main)")
    windowHasCleanedUp = True
    cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt catched")
        cleanup()
