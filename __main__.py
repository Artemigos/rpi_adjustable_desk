import RPi.GPIO as gpio
import asyncio as aio
import signal
import messages as msg
import engines
from state_machine import StateMachine
from time import sleep

print("Starting up...")

# pin numbers
OUT_UP = 23
OUT_DOWN = 24
BTN_UP = 19
BTN_DOWN = 26
BTN_UP_LONG = 6
BTN_DOWN_LONG = 13

print("Output pin for going up: ", OUT_UP)
print("Output pin for going down: ", OUT_DOWN)
print("Input pin for going up: ", BTN_UP)
print("Input pin for going down: ", BTN_DOWN)
print("Input pin for going all the way up: ", BTN_UP_LONG)
print("Input pin for going all the way down: ", BTN_DOWN_LONG)

# set pin numbering mode
gpio.setmode(gpio.BCM)

# set pin's in/out mode
gpio.setup([OUT_UP, OUT_DOWN], gpio.OUT)
gpio.setup(
        [BTN_UP, BTN_DOWN, BTN_UP_LONG, BTN_DOWN_LONG],
        gpio.IN,
        pull_up_down=gpio.PUD_DOWN)

# initialize outputs
engines.initialize(OUT_UP, OUT_DOWN)

# set up producer-consumer pattern
QUEUE = aio.Queue()

async def timer_producer():
    while True:
        await aio.sleep(1)
        await QUEUE.put(msg.SECOND_PASSED)

async def consumer():
    sm = StateMachine()
    while True:
        message = await QUEUE.get()
        sm.process(message)

LOOP = aio.get_event_loop()
LOOP.create_task(consumer())
LOOP.create_task(timer_producer())

# start reacting to input
MSG_MAP = {
        BTN_UP: (msg.UP_PRESSED, msg.UP_RELEASED),
        BTN_DOWN: (msg.DOWN_PRESSED, msg.DOWN_RELEASED),
        BTN_UP_LONG: (msg.UP_LONG_PRESSED, msg.UP_LONG_RELEASED),
        BTN_DOWN_LONG: (msg.DOWN_LONG_PRESSED, msg.DOWN_LONG_RELEASED) }

async def input_callback(channel):
    press, release = MSG_MAP[channel]
    if gpio.input(channel):
        print("[debug] got rising input from channel", channel)
        await QUEUE.put(press)
    else:
        print("[debug] got falling input from channel", channel)
        await QUEUE.put(release)

for k in MSG_MAP:
    gpio.add_event_detect(k, gpio.BOTH, bouncetime=100)

async def input_producer():
    while True:
        for k in MSG_MAP:
            if gpio.event_detected(k):
                await input_callback(k)
        await aio.sleep(0.05)

LOOP.create_task(input_producer())

# close when terminated
for sig in ('SIGINT', 'SIGTERM'):
    LOOP.add_signal_handler(getattr(signal, sig), LOOP.stop)

# start operating
try:
    print("Ready for input")
    LOOP.run_forever()
finally:
    # clean up after execution
    print("Cleaning up...")
    LOOP.close()
    gpio.cleanup()

