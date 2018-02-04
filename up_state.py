from state import State
import engines
import idle_state as ids
import long_up_state as lus

class UpState(State):
    def __init__(self):
        engines.up_on()

    def on_up_released(self):
        return ids.IdleState()

    def on_down_pressed(self):
        return self.on_up_released()

    def on_down_long_pressed(self):
        return self.on_up_released()

    def on_up_long_pressed(self):
        return lus.LongUpState()

