import messages

class State():
    def process(self, msg):
        return self._dispatch(msg)

    def _dispatch(self, msg):
        if hasattr(self, msg):
            handler = getattr(self, msg)
            return handler()

