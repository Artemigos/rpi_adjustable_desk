from state import State
import engines
from up_state import UpState
from down_state import DownState
from long_up_state import LongUpState
from long_down_state import LongDownState

class IdleState(State):
    def __init__(self):
        engines.up_off()
        engines.down_off()

    def on_up_pressed(self):
        return UpState()

    def on_down_pressed(self):
        return DownState()

    def on_up_long_pressed(self):
        return LongUpState()

    def on_down_long_pressed(self):
        return LongDownState()

