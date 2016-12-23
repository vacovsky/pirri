import pika
import config as CONFIG
import json
from psutil import Process

print(Process().name())
if Process().name() == 'pirri':
    from helpers.RelayControl import RelayController
else:
    from helpers.RelayControlFake import RelayControllerFake as RelayController


class RMQ:
    CHANNEL = None
    CONNECTION = None
    queue = None

    def __init__(self):
        self.queue = CONFIG.SETTINGS['RMQ_QUEUE']

    def publish_message(self, message):
        self.publish_messages([message])

    def publish_messages(self, messages=[]):
        self.open_connection()
        for message in messages:
            self.CHANNEL.queue_declare(queue=self.queue)
            self.CHANNEL.basic_publish(exchange='',
                                       routing_key=self.queue,
                                       body=message)
            print(" [x] Sent %s" % message)
        self.close_connection()

    def open_connection(self):
        self.CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
            heartbeat_interval=0,
            host=CONFIG.SETTINGS['RMQ_HOST']))
        self.CHANNEL = self.CONNECTION.channel()

    def close_connection(self):
        self.CONNECTION.close()

    def callback(self, ch, method, properties, body):
        try:
            jobdata = body.decode("utf-8")
            job = json.loads(jobdata)
            # DO SOMETHING HERE
            print(job)
            if 'schedule_id' not in job:
                job['schedule_id'] = 0
            RelayController().activate_relay(
                job['sid'],
                job['duration'],
                job['schedule_id'])

        except Exception as e:
            print(e)

    def ack_job(self, ch, method):
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def listen(self):
        self.open_connection()
        self.CHANNEL.queue_declare(queue=self.queue)
        self.CHANNEL.basic_consume(self.callback,
                                   queue=self.queue,
                                   no_ack=True)

        print(
            ' [*] Waiting for messages on "{0}". To exit press CTRL+C'.format(self.queue))
        self.CHANNEL.start_consuming()


if __name__ == '__main__':
    listen = RMQ()
    listen.listen()
