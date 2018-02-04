from idle_state import IdleState

class StateMachine():
    def __init__(self):
        self.state = IdleState()

    def process(self, msg):
        new_state = self.state.process(msg)
        if new_state != None:
            self.state = new_state

