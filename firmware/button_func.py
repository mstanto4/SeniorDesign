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
BUT_P_B = 23
BUT_P_G = 23
BUT_P_Y = 24
BUT_P_R = 25

LED_C_W = 5
LED_C_B = 6
LED_C_G = 13
LED_C_Y = 19
LED_C_R = 26

# Button flash time (in seconds)
FLASH_TIME = 0.5

# Sets up RPi GPIOs and all above specified pins
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.Board)

    # Set up the direction and default values of pins

    # Player
    GPIO.setup(LED_P_W, GPIO.OUT)
    GPIO.setup(LED_P_B, GPIO.OUT)
    GPIO.setup(LED_P_G, GPIO.OUT)
    GPIO.setup(LED_P_Y, GPIO.OUT)
    GPIO.setup(LED_P_R, GPIO.OUT)

    GPIO.setup(BUT_P_W, GPIO.IN)
    GPIO.setup(BUT_P_B, GPIO.IN)
    GPIO.setup(BUT_P_G, GPIO.IN)
    GPIO.setup(BUT_P_Y, GPIO.IN)
    GPIO.setup(BUT_P_R, GPIO.IN)

    # Neural network
    GPIO.setup(LED_C_W, GPIO.OUT)
    GPIO.setup(LED_C_B, GPIO.OUT)
    GPIO.setup(LED_C_G, GPIO.OUT)
    GPIO.setup(LED_C_Y, GPIO.OUT)
    GPIO.setup(LED_C_R, GPIO.OUT)

# Reads the status of the five input player buttons and returns the
# result as a list of 1s and 0s. 1 means the button was pressed, 0
# means the button was not pressed. This function also flashes the
# LED of the corresponding button if the button was pressed.
def read_button():
    # List holding what buttons are read to be high
    button_vals = [False,False,False,False,False]

    # Button value is pulled LOW when pressed due to pull up resistor.
    if GPIO.input(BUT_P_W) == GPIO.LOW:
        GPIO.output(LED_P_W, GPIO.LOW)
        sleep(FLASH_TIME)
        GPIO.output(LED_P_W, GPIO.LOW)
        button_vals[0] = True

    if GPIO.input(BUT_P_B) == GPIO.LOW:
        GPIO.output(LED_P_B, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_P_B, GPIO.LOW)
        button_vals[1] = True

    if GPIO.input(BUT_P_G) == GPIO.LOW:
        GPIO.output(LED_G_B, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_G_B, GPIO.LOW)
        button_vals[2] = True

    if GPIO.input(BUT_P_Y) == GPIO.LOW:
        GPIO.output(LED_G_Y, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_G_Y, GPIO.LOW)
        button_vals[3] = True

    if GPIO.input(BUT_P_R) == GPIO.LOW:
        GPIO.output(LED_G_R, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_G_R, GPIO.LOW)
        button_vals[4] = True

    return button_vals

# This function takes a list of 5 values of 0s or 1s, and flashes the
# corresponding button for values of 1.
def flash_led(buttons):
    if buttons[0] == True:
        GPIO.output(LED_C_W, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_C_W, GPIO.LOW)

    if buttons[1] == True:
        GPIO.output(LED_C_B, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_C_B, GPIO.LOW)

    if buttons[2] == True:
        GPIO.output(LED_C_G, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_C_G, GPIO.LOW)

    if buttons[3] == True:
        GPIO.output(LED_C_Y, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_C_Y, GPIO.LOW)

    if buttons[4] == True:
        GPIO.output(LED_C_R, GPIO.HIGH)
        sleep(FLASH_TIME)
        GPIO.output(LED_C_R, GPIO.LOW)

def cleanup():
    GPIO.cleanup()

