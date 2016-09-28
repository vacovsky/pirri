import pika
from data import config as CONFIG
import json
from threading import Thread


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

    def sp_exec(self, action, job):
        print(job)
        if action == "destroy":
            print("destroying " + job['cookbook'])
            Thread(target=Kitchen().destroy_kitchen, args=(job['cookbook'], job['cookbook_root'],
                                                           job['kitchen_bin']))
        elif action == "converge":
            print("converging " + job['cookbook'])
            Thread(target=Kitchen().start_kitchen, args=(job['cookbook'], job['cookbook_root'],
                                                         job['kitchen_bin']))
        else:
            pass

    def callback_2(self, ch, method, properties, body):
        jobdata = body.decode("utf-8")
        job = json.loads(jobdata)
        # DO SOMETHING HERE
        kitchen = Kitchen()
        vm_running = kitchen.check_running()
        if vm_running:
            print(
                "VM is already running.  Please close any open virtual machines and re-submit job to use this agent.")
            self.ack_job(ch, method)
        else:
            try:
                print("Working in the kitchen, please wait...")
                if job['destroy'] == "true":
                    self.sp_exec('destroy', job)
                elif job['destroy'] == "false":
                    self.sp_exec('converge', job)
                else:
                    print("nothing to see here...")

            except Exception as e:
                print("failure.  check your settings.  error follows.")
                print(e)
            finally:
                if True:
                    self.ack_job(ch, method)
                print("task complete.")

    def callback(self, ch, method, properties, body):
        self.ack_job(ch, method)
        jobdata = body.decode("utf-8")
        job = json.loads(jobdata)
        # DO SOMETHING HERE
        kitchen = Kitchen()
        print("ALIVE!")
        try:
            if job['destroy'] == 'false':
                kitchen.start_kitchen(job['cookbook'], job['cookbook_root'],
                                      job['kitchen_bin'])
            if job['destroy'] == 'true':
                kitchen.destroy_kitchen(job['cookbook'], job['cookbook_root'],
                                        job['kitchen_bin'])

        except Exception as e:
            print("failure.  check your settings.  error follows.")
            print(e)
        finally:
            print("task complete.")

    def ack_job(self, ch, method):
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def listen(self, queue=CONFIG.QUEUE):
        self.open_connection()
        self.CHANNEL.queue_declare(queue=queue)
        self.CHANNEL.basic_consume(self.callback,
                                   queue=queue,
                                   no_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.CHANNEL.start_consuming()


if __name__ == '__main__':
    listen = RMQ()
    listen.listen()
