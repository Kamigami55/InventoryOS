import RPi.GPIO as GPIO
import threading
from time import sleep

# Pin assignment
Enc_A = 16
Enc_B = 18
BUTTON = 22
BUZZER = 12


Rotary_counter = 0
Current_A = 1 
Current_B = 1

LockRotary = threading.Lock()       # create lock for rotary switch
    

# initialize interrupt handlers
def init():
    global buzzer
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    
    # Rotary encoder gpio setting
    GPIO.setup(Enc_A, GPIO.IN)              
    GPIO.setup(Enc_B, GPIO.IN)
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt)
    GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt)

    # Button gpio setting
    GPIO.setup(BUTTON, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_interrupt, bouncetime=300)

    # Buzzer gpio setting
    GPIO.setup(BUZZER, GPIO.OUT)
    buzzer = GPIO.PWM(BUZZER, 50)


# Button intrrupt
def button_interrupt(event):
    print "Button pressed"
    buzzer.ChangeFrequency(300)
    buzzer.start(50)
    sleep(0.2)
    buzzer.stop()
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
            print "R+ %d" % Rotary_counter
            buzzer.ChangeFrequency(200)
        else:
            Rotary_counter -= 1
            print "R- %d" % Rotary_counter
            buzzer.ChangeFrequency(150)
        LockRotary.release() # release lock
        buzzer.start(50)
        sleep(0.1)
        buzzer.stop()
    return


def main():
    global Rotary_counter, LockRotary

    Volume = 0
    NewCounter = 0

    init()

    while True :
        pass

    GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()

GPIO.cleanup()


