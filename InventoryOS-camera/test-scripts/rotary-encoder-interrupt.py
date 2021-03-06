import RPi.GPIO as GPIO
import threading
from time import sleep

Enc_A = 16
Enc_B = 18

Rotary_counter = 0
Current_A = 1 
Current_B = 1

LockRotary = threading.Lock()       # create lock for rotary switch
    

# initialize interrupt handlers
def init():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Enc_A, GPIO.IN)              
    GPIO.setup(Enc_B, GPIO.IN)
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt)
    GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt)
    return


# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):
    global Rotary_counter, Current_A, Current_B, LockRotary
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)
    
    # now check if state of A or B has changed
    # if not that means that bouncing caused it
    if Current_A == Switch_A and Current_B == Switch_B: # Same interrupt as before (Bouncing)?
        return # ignore interrupt!

    Current_A = Switch_A # remember new state, for next bouncing check
    Current_B = Switch_B

    # Both one active? Yes -> end of sequence
    if (Switch_A and Switch_B):
        LockRotary.acquire() # get lock 
        if A_or_B == Enc_B: # Turning direction depends on 
            Rotary_counter += 1
        else:
            Rotary_counter -= 1
        LockRotary.release() # release lock
    return


def main():
    global Rotary_counter, LockRotary

    Volume = 0
    NewCounter = 0

    init()

    while True :
        sleep(0.1) # sleep 100ms

        LockRotary.acquire() # get lock for rotary switch
        NewCounter = Rotary_counter
        Rotary_counter = 0
        LockRotary.release()

        if (NewCounter !=0): # Counter has CHANGED
            Volume = Volume + NewCounter*abs(NewCounter)
            if Volume < 0:
                Volume = 0
            if Volume > 100:
                Volume = 100
            print NewCounter, Volume

main()

