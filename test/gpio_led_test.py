import RPi.GPIO as gpio
from time import sleep

PIN = [23, 24, 22, 27, 17]
STEPS = 10

gpio.setmode(gpio.BCM)
gpio.setup(PIN, gpio.OUT)

for i in range(0, STEPS):
    gpio.output(PIN, i % 2)
    print("Blinking step %d/%d" % (i + 1, STEPS))
    sleep(1)

gpio.cleanup()

