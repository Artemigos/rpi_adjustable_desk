import RPi.GPIO as gpio
from time import sleep

LED = 23
LED_STATE = 0

LED_BTN = 19
EXIT_BTN = 13

gpio.setmode(gpio.BCM)
gpio.setup(LED, gpio.OUT)
gpio.setup([LED_BTN, EXIT_BTN], gpio.IN, pull_up_down=gpio.PUD_DOWN)

gpio.add_event_detect(LED_BTN, gpio.RISING)

def set_led(val):
    print("Setting LED to", val)
    global LED_STATE
    LED_STATE = val
    gpio.output(LED, val)

def toggle_led():
    set_led(1 - LED_STATE)

set_led(1)

while True:
    if gpio.input(EXIT_BTN):
        print("Exit button clicked")
        break
    if gpio.event_detected(LED_BTN):
        print("Toggle button clicked")
        toggle_led()
    sleep(0.05)

gpio.cleanup()

