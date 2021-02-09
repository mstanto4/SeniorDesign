'''
Title: test_buttons.py
Date: February 7, 2021
Written by: Samantha Zimmermann
Description: Tests the functions in button_func.py. Takes a command line argument "button" or "led" to specify which
function to test. Uses GPIO pin 9 to test LED, GPIO pin 25 to test Button press.
'''

from time import sleep
import button_func as bf
import sys

# Test with red button only
LED = 9
BUT = 25

bf.setup()

# Test button press
if sys.argv[1] = "button":
    try:
        while True:
            vals = read_button()
            if vals[4] == 1:
                print("Red button pressed!")

    except KeyboardInterrupt:
        bf.cleanup()

# Test LED Flash
else if sys.argv[1] = "led":
    try:
        while True:
            flash_led([0, 0, 0, 0, 1])
            sleep(1)

    except KeyboardInterrupt:
        bf.cleanup()

else:
    print("Invalid test")

