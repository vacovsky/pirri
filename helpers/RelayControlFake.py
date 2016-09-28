
class RelayControllerFake:

    def __init__(self):
        print('FAKE: init RelayControllerFake;')

    def log_relay_activity(self, sid, duration, schedule_id=0):
        print('FAKE: log_relay_activity; sid={0}, duration={1}, schedule_id={2}'.format(
            sid, duration, schedule_id))

    def activate_relay(self, sid):
        print('FAKE: activate_relay;  sid={0}'.format(sid))
