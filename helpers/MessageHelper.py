import pika
from data import config as CONFIG
import json
# from threading import Thread
from psutil import Process

print(Process().name())
if Process().name() == 'pirri':
    from helpers.RelayControl import RelayController
else:
    from helpers.RelayControlFake import RelayControllerFake as RelayController


class RMQ:
    CHANNEL = None
    CONNECTION = None

    def __init__(self):
        pass

    def publish_message(self, message, queue=CONFIG.QUEUE):
        self.publish_messages([message], queue)

    def publish_messages(self, messages=[], queue=CONFIG.QUEUE):
        self.open_connection()
        for message in messages:
            self.CHANNEL.queue_declare(queue=queue)
            self.CHANNEL.basic_publish(exchange='',
                                       routing_key=queue,
                                       body=message)
            print(" [x] Sent %s" % message)
        self.close_connection()

    def open_connection(self):
        self.CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
            host=CONFIG.RMQ_HOST,
            port=CONFIG.RMQ_PORT,
            credentials=pika.credentials.PlainCredentials(
                CONFIG.RMQ_USER,
                CONFIG.RMQ_PASS),))
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
            # Thread(target=RelayController(CONFIG.COMMON_WIRE_GPIO).activate_relay(),
            # args=(job['sid'], job['duration'], job['schedule_id'])).start()

        except Exception as e:
            print(e)
        #finally:
        #    self.ack_job(ch, method)

    def ack_job(self, ch, method):
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def listen(self, queue=CONFIG.QUEUE):
        self.open_connection()
        self.CHANNEL.queue_declare(queue=queue)
        self.CHANNEL.basic_consume(self.callback,
                                   queue=queue,
                                   no_ack=True)

        print(
            ' [*] Waiting for messages on "{0}". To exit press CTRL+C'.format(queue))
        self.CHANNEL.start_consuming()


if __name__ == '__main__':
    listen = RMQ()
    listen.listen()
