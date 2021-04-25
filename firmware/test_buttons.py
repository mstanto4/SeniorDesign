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

bf.setup()

# Test button press
if sys.argv[1] == "button":
    try:
        while True:
            vals = bf.read_button()
            print(vals[0])
            if vals[0] == True:
                print("White button pressed!")

    except KeyboardInterrupt:
        bf.cleanup()

# Test LED Flash
elif sys.argv[1] == "led":
    try:
        while True:
            bf.flash_led([True, True, True, True, True])
            sleep(200);
            bf.flash_led([False, False, False, False, False])
            sleep(200);

    except KeyboardInterrupt:
        bf.cleanup()

else:
    print("Invalid test -- specify 'button' or 'led'")

