import RPi.GPIO as GPIO # Import RPi GPIO library

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

# Sets up RPi GPIOs and all above specified pins
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.Board)

    # Set up the direction and default values of pins
    GPIO.setup(LED_P_W, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_P_B, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_P_G, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_P_Y, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_P_R, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);

    GPIO.setup(LED_C_W, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_C_B, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_C_G, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_C_Y, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(LED_C_R, GPIO.OUT, pull_up_down=GPIO_PUD_DOWN);

    GPIO.setup(BUT_P_W, GPIO.IN, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(BUT_P_B, GPIO.IN, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(BUT_P_G, GPIO.IN, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(BUT_P_Y, GPIO.IN, pull_up_down=GPIO_PUD_DOWN);
    GPIO.setup(BUT_P_R, GPIO.IN, pull_up_down=GPIO_PUD_DOWN);

# Reads the status of the five input player buttons and returns the
# result as a list of 1s and 0s. 1 means the button was pressed, 0
# means the button was not pressed. This function also flashes the
# LED of the corresponding button if the button was pressed.

# FIXME: Not tested with all buttons.
def read_button():
    # List holding what buttons are read to be high
    button_vals = [0,0,0,0,0]

    if GPIO.input(BUT_P_W) == GPIO.HIGH:
        print("White button was pushed!")
        GPIO.output(LED_P_W, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_P_W, GPIO.LOW);
        button_vals[0] = 1;
    if GPIO.input(BUT_P_B) == GPIO.HIGH:
        GPIO.output(LED_P_B, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_P_B, GPIO.LOW);
        button_vals[1] = 1;
    if GPIO.input(BUT_P_G) == GPIO.HIGH:
        GPIO.output(LED_G_B, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_G_B, GPIO.LOW);
        button_vals[2] = 1;
    if GPIO.input(BUT_P_Y) == GPIO.HIGH:
        GPIO.output(LED_G_Y, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_G_Y, GPIO.LOW);
        button_vals[3] = 1;
    if GPIO.input(BUT_P_R) == GPIO.HIGH:
        GPIO.output(LED_G_R, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_G_R, GPIO.LOW);
        button_vals[4] = 1;

    return button_vals;

# This function takes a list of 5 values of 0s or 1s, and flashes the
# corresponding button for values of 1.

# FIXME: Not tested with all buttons.
def flash_led(buttons):
    if buttons[0] == 1:
        GPIO.output(LED_C_W, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_C_W, GPIO.LOW);
    if buttons[1] == 1:
        GPIO.output(LED_C_B, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_C_B, GPIO.LOW);
    if buttons[2] == 1:
        GPIO.output(LED_C_G, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_C_G, GPIO.LOW);
    if buttons[3] == 1:
        GPIO.output(LED_C_Y, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_C_Y, GPIO.LOW);
    if buttons[4] == 1:
        GPIO.output(LED_C_R, GPIO.HIGH);
        time.sleep(1);
        GPIO.output(LED_C_R, GPIO.LOW);

