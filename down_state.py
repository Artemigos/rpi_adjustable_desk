from state import State
import engines
import idle_state as ids
import long_down_state as lds

class DownState(State):
    def __init__(self):
        engines.down_on()

    def on_down_released(self):
        return ids.IdleState()

    def on_up_pressed(self):
        return self.on_down_released()

    def on_up_long_pressed(self):
        return self.on_down_released()

    def on_down_long_pressed(self):
        return lds.LongDownState()

