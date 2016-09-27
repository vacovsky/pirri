import RPi.GPIO as GPIO

#  Do I use a redis pubsub for this?


class RelayController:
    common = None
    relays = []

    def __init__(self, common, relays):
        self.setup_pins(common, relays)

    def setup_pins(self):
        pass

    def __reset(self):
        pass

    def activate_relay(self):
        self.__reset()
        pass
