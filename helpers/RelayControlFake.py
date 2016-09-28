
class RelayControllerFake:

    def __init__(self):
        print('FAKE: init RelayControllerFake;')

    def activate_relay(self, sid, duration, schedule_id=0):
        print('FAKE: activate_relay;  sid={0}'.format(sid))
