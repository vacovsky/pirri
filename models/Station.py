import RPi.GPIO as GPIO


class Station:
    pin = None
    state = 1
    location = ""
    active_ttl = 0

    def __init__(self, state=None):
        self.state = state or 1

    def activate(self, time=900):
        pass

    def deactivate(self):
        pass

    def status(self):
        return self.pin, self.state, self.location, self.active_ttl
