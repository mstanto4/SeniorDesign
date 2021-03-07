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
if sys.argv[1] == "button":
    try:
        while True:
            vals = bf.read_button()
            print(vals[4])
            if vals[4] == True:
                print("Red button pressed!")

    except KeyboardInterrupt:
        bf.cleanup()

# Test LED Flash
elif sys.argv[1] == "led":
    try:
        while True:
            bf.flash_led([0, 0, 0, 0, 1])
            sleep(1)

    except KeyboardInterrupt:
        bf.cleanup()

else:
    print("Invalid test -- specify 'button' or 'led'")

