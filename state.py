import messages

class State():
    def process(self, msg):
        return self._dispatch(msg)

    def on_up_pressed(self):
        return self
    
    def on_up_released(self):
        return self

    def on_down_pressed(self):
        return self

    def on_down_released(self):
        return self

    def on_up_long_pressed(self):
        return self

    def on_up_long_released(self):
        return self

    def on_down_long_pressed(self):
        return self

    def on_down_long_released(self):
        return self

    def on_second_passed(self):
        return self

    def _dispatch(self, msg):
        if msg == messages.SECOND_PASSED:
            return self.on_second_passed()
        elif msg == messages.UP_PRESSED:
            return self.on_up_pressed()
        elif msg == messages.UP_RELEASED:
            return self.on_up_released()
        elif msg == messages.DOWN_PRESSED:
            return self.on_down_pressed()
        elif msg == messages.DOWN_RELEASED:
            return self.on_down_released()
        elif msg == messages.UP_LONG_PRESSED:
            return self.on_up_long_pressed()
        elif msg == messages.UP_LONG_RELEASED:
            return self.on_up_long_released()
        elif msg == messages.DOWN_LONG_PRESSED:
            return self.on_down_long_pressed()
        elif msg == messages.DOWN_LONG_RELEASED:
            return self.on_down_long_released()
        else:
            print("Unknown message ignored:", msg)

