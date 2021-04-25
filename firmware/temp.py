'''
Title: button_func.py
Date: January 28, 2021
Written by: Samantha Zimmermann 
Description: Definition of LED and button GPIO pin constants. Contains setup function, which configures RPi GPIO pins; read_button, which returns
a list of 1s and 0s corresponding to if a player button has been pressed and flashes the player button's LED for the configured amount of time; and flash_led, 
which takes a list of 1s and 0s, and flashes the corresponding neural network player LED for the configured amount of time; and cleanup, which simply calls
the GPIO cleanup function.
'''
import RPi.GPIO as GPIO # Import RPi GPIO library
from time import sleep  # Delay function

# "Constants" holding pin numbers for player and network buttons
LED_P_W = 17
LED_P_B = 27
LED_P_G = 22
LED_P_Y = 10
LED_P_R = 9

BUT_P_W = 15
BUT_P_B = 18
BUT_P_G = 23
BUT_P_Y = 24
BUT_P_R = 25

LED_C_W = 5
LED_C_B = 6
LED_C_G = 13
LED_C_Y = 19
LED_C_R = 26

# Button flash time (in seconds)
FLASH_TIME = 0.05

# Debouncer logic
lastpinval = [GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]

# Sets up RPi GPIOs and all above specified pins
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Set up the direction and default values of pins

    # Player
    GPIO.setup(LED_P_W, GPIO.OUT)
    GPIO.setup(LED_P_B, GPIO.OUT)
    GPIO.setup(LED_P_G, GPIO.OUT)
    GPIO.setup(LED_P_Y, GPIO.OUT)
    GPIO.setup(LED_P_R, GPIO.OUT)

    GPIO.setup(BUT_P_W, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUT_P_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUT_P_G, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUT_P_Y, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUT_P_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Neural network
    GPIO.setup(LED_C_W, GPIO.OUT)
    GPIO.setup(LED_C_B, GPIO.OUT)
    GPIO.setup(LED_C_G, GPIO.OUT)
    GPIO.setup(LED_C_Y, GPIO.OUT)
    GPIO.setup(LED_C_R, GPIO.OUT)

# Reads the status of the five input player buttons and returns the
# result as a list of 1s and 0s. 1 means the button was pressed, 0
# means the button was not pressed.
def read_button():
    # List holding what buttons are read to be high
    button_vals = [False,False,False,False,False]

    # Button value is pulled LOW when pressed due to pull up resistor.
    if GPIO.input(BUT_P_W) == GPIO.HIGH and lastpinval[4] == GPIO.LOW:
        button_vals[4] = True

    if GPIO.input(BUT_P_B) == GPIO.HIGH and lastpinval[3] == GPIO.LOW:
        button_vals[3] = True

    if GPIO.input(BUT_P_G) == GPIO.HIGH and lastpinval[2] == GPIO.LOW:
        button_vals[2] = True

    if GPIO.input(BUT_P_Y) == GPIO.HIGH and lastpinval[1] == GPIO.LOW:
        button_vals[1] = True

    if GPIO.input(BUT_P_R) == GPIO.HIGH and lastpinval[0] == GPIO.LOW:
        button_vals[0] = True

    lastpinval[4] = GPIO.input(BUT_P_W)
    lastpinval[3] = GPIO.input(BUT_P_B)
    lastpinval[2] = GPIO.input(BUT_P_G)
    lastpinval[1] = GPIO.input(BUT_P_Y)
    lastpinval[0] = GPIO.input(BUT_P_R)

    return button_vals

# This function takes a pin number and a boolean activate. If activate
# is true, the LED is turned on. If activate is false, the LED is turned 
# off.
def flash_led(pin, activate):
    if activate == True:
        GPIO.output(pin, GPIO.HIGH)
    if activate == False:
        GPIO.output(pin, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

# Test code
# setup()
 
# try:
#    while True:
#         test = read_button()
#        print(test)
         
#except KeyboardInterrupt:
#   cleanup()


