import RPi.GPIO as gpio

class Output():
    def __init__(self, pin, on_state = 0, name = ""):
        self.pin = pin
        self.on_state = on_state
        self.name = name
        self.off_state = 1 - on_state
        gpio.setup(pin, gpio.OUT)
        self.off()
        print("[debug] set up pin", pin, "to be an output")

    def off(self):
        gpio.output(self.pin, self.off_state)
        self.current = self.off_state

    def on(self):
        gpio.output(self.pin, self.on_state)
        self.current = self.on_state

class Input():
    def __init__(self, pin, pull = gpio.PUD_DOWN, name = ""):
        self.pin = pin
        self.name = name
        gpio.setup(pin, gpio.IN, pull_up_down = pull)
        self._last_value = self.read()
        print("[debug] set up pin", pin, "to be an input")

    def read(self):
        return gpio.input(self.pin)

    def event_detected(self):
        return self._process_input()

    async def dispatch_detected_event(self, on_rising, on_falling):
        event = self.event_detected()
        if event is not None:
            if event == gpio.RISING:
                await on_rising(self)
            else:
                await on_falling(self)

    def _process_input(self):
        current = self.read()
        if current != self._last_value:
            self._last_value = current
            if current == 1:
                return gpio.RISING
            else:
                return gpio.FALLING

class IOContainer():
    class _placeholder: pass

    def __init__(self):
        self.i = IOContainer._placeholder()
        self.o = IOContainer._placeholder()

    def add_inputs(self, **kwargs):
        for k in kwargs:
            v = kwargs[k]
            setattr(self.i, k, Input(v, name = k))

    def add_outputs(self, on_state = 0, **kwargs):
        for k in kwargs:
            v = kwargs[k]
            setattr(self.o, k, Output(v, on_state, k))

    def inputs(self):
        return self.i.__dict__

    def outputs(self):
        return self.o.__dict__

    def input(self, name):
        return self.inputs()[name]

    def output(self, name):
        return self.outputs()[name]

    async def dispatch_input_events(self, on_rising, on_falling):
        for k in self.inputs():
            await self.input(k).dispatch_detected_event(on_rising, on_falling)

    def summary(self):
        for k in self.inputs():
            print("Input pin '{}': {}".format(k, self.input(k).pin))
        for k in self.outputs():
            print("Output pin '{}': {}".format(k, self.output(k).pin))

