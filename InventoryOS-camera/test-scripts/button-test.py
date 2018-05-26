import RPi.GPIO as GPIO

BUTTON = 22

# initialize interrupt handlers
def init():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_interrupt, bouncetime=300)
    return


def button_interrupt(event):
    print "Button pressed"
    return


def main():

    init()

    while True :
        pass

main()

