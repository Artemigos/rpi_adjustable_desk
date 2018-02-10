from state import State
import engines
import idle_state as ids
import up_state as us
import down_state as ds
import long_down_state as lds

class LongUpState(State):
    def __init__(self, length=20):
        self.length = length
        self.current_time = 0
        engines.up_on()

    def on_second_passed(self):
        self.current_time += 1
        if self.current_time >= self.length:
            return ids.IdleState()

    def on_up_pressed(self):
        return us.UpState()

    def on_down_pressed(self):
        return ds.DownState()

    def on_down_long_pressed(self):
        return lds.LongDownState()

