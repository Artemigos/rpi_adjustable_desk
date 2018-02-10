from idle_state import IdleState

class StateMachine():
    def __init__(self):
        self.state = IdleState()

    def process(self, msg):
        new_state = self.state.process(msg)
        if new_state != None:
            print("[debug] changing state from", self._get_name(self.state), "to", self._get_name(new_state))
            self.state = new_state

    def _get_name(self, obj):
        t = type(obj)
        if t.__name__ == 'function':
            return obj.__name__
        else:
            return t.__name__

