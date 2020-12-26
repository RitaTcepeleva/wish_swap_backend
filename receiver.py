import pika
import os
import traceback
import threading
import json
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wish_swap.settings')
import django
django.setup()

from wish_swap.settings import BLOCKCHAINS


class Receiver(threading.Thread):
    def __init__(self, blockchain):
        super().__init__()
        self.blockchain = blockchain

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'rabbitmq',
            5672,
            os.getenv('RABBITMQ_DEFAULT_VHOST', 'wish_swap'),
            pika.PlainCredentials(os.getenv('RABBITMQ_DEFAULT_USER', 'wish_swap'), os.getenv('RABBITMQ_DEFAULT_PASS', 'wish_swap')),
        ))
        channel = connection.channel()
        channel.queue_declare(
                queue=self.blockchain,
                durable=True,
                auto_delete=False,
                exclusive=False
        )
        channel.basic_consume(
            queue=self.blockchain,
            on_message_callback=self.callback
        )
        print(f'receiver: `{self.blockchain}` queue was started', flush=True)
        channel.start_consuming()

    def payment(self, message):
        message['from_blockchain'] = self.blockchain
        print('receiver: Payment message has been received', flush=True)
        # parse_payment_message(message)

    def callback(self, ch, method, properties, body):
        print('receiver: Received message data:', method, properties, body, flush=True)
        try:
            message = json.loads(body.decode())
            if message.get('status', '') == 'COMMITTED':
                getattr(self, properties.type, self.unknown_handler)(message)
        except Exception as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())),
                  flush=True)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def unknown_handler(self, message):
        print('receiver: Unknown message has been received', message, flush=True)


for blockchain in BLOCKCHAINS.keys():
    receiver = Receiver(blockchain)
    receiver.start()
