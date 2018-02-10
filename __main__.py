import RPi.GPIO as gpio
import asyncio as aio
import signal
import messages as msg
import engines
from state_machine import StateMachine
from wrapped_io import IOContainer

print("Starting up...")

# set pin numbering mode
gpio.setmode(gpio.BCM)

# IO setup
IO = IOContainer()
IO.add_outputs(
        main = 17,
        left_up = 23,
        left_down = 22,
        right_up = 27,
        right_down = 24)
IO.add_inputs(
        up = 19,
        down = 26,
        up_long = 6,
        down_long = 13)

IO.summary()

# initialize engines
engines.initialize(IO.o)

# set up producer-consumer pattern
QUEUE = aio.Queue()

async def timer_producer():
    while True:
        await aio.sleep(1)
        await QUEUE.put("on_second_passed")

async def consumer():
    sm = StateMachine()
    while True:
        message = await QUEUE.get()
        sm.process(message)

LOOP = aio.get_event_loop()
LOOP.create_task(consumer())
LOOP.create_task(timer_producer())

# start reacting to input
async def rising_callback(channel):
    event = "on_" + channel.name + "_pressed"
    print("[debug] got rising input from channel", channel.pin)
    await QUEUE.put(event)

async def falling_callback(channel):
    event = "on_" + channel.name + "_released"
    print("[debug] got falling input from channel", channel.pin)
    await QUEUE.put(event)

async def input_producer():
    while True:
        await IO.dispatch_input_events(rising_callback, falling_callback)
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

