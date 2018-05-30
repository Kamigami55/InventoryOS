#!/usr/local/bin/python
import time
import RPi.GPIO as GPIO

BUZZER = 12

def doReMi():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER, GPIO.OUT)
    p = GPIO.PWM(BUZZER, 50)
    p.start(50)

    print("Do")
    p.ChangeFrequency(523)
    time.sleep(1)

    print("Re")
    p.ChangeFrequency(587)
    time.sleep(1)
   
    print("Mi")
    p.ChangeFrequency(659)
    time.sleep(1)

    p.stop()
    GPIO.cleanup()

doReMi()
