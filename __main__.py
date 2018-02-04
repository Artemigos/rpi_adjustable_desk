import RPi.GPIO as gpio
import asyncio as aio
import signal
import messages as msg
import engines
from state_machine import StateMachine
import wrapped_io as io

print("Starting up...")

# pin numbers
OUT_MAIN = 17
OUT_LEFT_UP = 23
OUT_LEFT_DOWN = 22
OUT_RIGHT_UP = 27
OUT_RIGHT_DOWN = 24

BTN_UP = 19
BTN_DOWN = 26
BTN_UP_LONG = 6
BTN_DOWN_LONG = 13

print("Output pin for main power:", OUT_MAIN)
print("Output pin for left engine going up: ", OUT_LEFT_UP)
print("Output pin for left engine going down: ", OUT_LEFT_UP)
print("Output pin for right engine going up: ", OUT_LEFT_UP)
print("Output pin for right engine going down: ", OUT_RIGHT_DOWN)
print("Input pin for going up: ", BTN_UP)
print("Input pin for going down: ", BTN_DOWN)
print("Input pin for going all the way up: ", BTN_UP_LONG)
print("Input pin for going all the way down: ", BTN_DOWN_LONG)

# set pin numbering mode
gpio.setmode(gpio.BCM)

I_UP = io.Input(BTN_UP) 
I_DOWN = io.Input(BTN_DOWN) 
I_UP_LONG = io.Input(BTN_UP_LONG) 
I_DOWN_LONG = io.Input(BTN_DOWN_LONG) 

# set pin's in/out mode
gpio.setup(
        [OUT_MAIN, OUT_LEFT_UP, OUT_LEFT_DOWN, OUT_RIGHT_UP, OUT_RIGHT_DOWN],
        gpio.OUT)

# initialize outputs
engines.initialize(
        OUT_MAIN,
        OUT_LEFT_UP,
        OUT_LEFT_DOWN,
        OUT_RIGHT_UP,
        OUT_RIGHT_DOWN)

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
        I_UP: (msg.UP_PRESSED, msg.UP_RELEASED),
        I_DOWN: (msg.DOWN_PRESSED, msg.DOWN_RELEASED),
        I_UP_LONG: (msg.UP_LONG_PRESSED, msg.UP_LONG_RELEASED),
        I_DOWN_LONG: (msg.DOWN_LONG_PRESSED, msg.DOWN_LONG_RELEASED) }

async def rising_callback(channel):
    press, release = MSG_MAP[channel]
    print("[debug] got rising input from channel", channel.pin)
    await QUEUE.put(press)

async def falling_callback(channel):
    press, release = MSG_MAP[channel]
    print("[debug] got falling input from channel", channel.pin)
    await QUEUE.put(release)

async def input_producer():
    while True:
        for k in MSG_MAP:
            await k.dispatch_detected_event(rising_callback, falling_callback)
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

