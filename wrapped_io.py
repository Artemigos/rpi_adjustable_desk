import RPi.GPIO as gpio

class Output():
    def __init__(self, pin, on_state = 0):
        self.pin = pin
        self.on_state = on_state
        self.off_state = 1 - on_state
        gpio.setup(pin, gpio.OUT)
        self.off()
        print("[debug] set up pin", pin, "to be an output")

    def on(self):
        gpio.output(self.pin, self.off_state)
        self.current = self.off_state

    def off(self):
        gpio.output(self.pin, self.on_state)
        self.current = self.on_state

class Input():
    def __init__(self, pin, pull = gpio.PUD_DOWN):
        self.pin = pin
        gpio.setup(pin, gpio.IN, pull_up_down = pull)
        gpio.add_event_detect(pin, gpio.BOTH, bouncetime=100)
        print("[debug] set up pin", pin, "to be an input")

    def read(self):
        return gpio.input(self.pin)

    def event_detected(self):
        return gpio.event_detected(self.pin)

    async def dispatch_detected_event(self, on_rising, on_falling):
        if self.event_detected():
            print("[debug] event detected")
            if self.read():
                await on_rising(self)
            else:
                await on_falling(self)

