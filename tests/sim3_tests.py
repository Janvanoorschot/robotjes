import pika
import uuid
import unittest
import os

from robotjes.remote import Handler
from robotjes.sim import Engine, Map

DIR = os.path.dirname(os.path.abspath(__file__))


class Sim3TestCase(unittest.TestCase):

    def init(self):
        self.rmqhost = 'localhost'
        self.rmqport = 5672
        self.rmqqueue = 'rpc_queue'
        self.response = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def prepare(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rmqhost, port=self.rmqport))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,on_message_callback=self.on_response, auto_ack=True)

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.rmqqueue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

    def finalize(self):
        pass

    def test_sim301(self):
        response = self.call("robo.forward(1)")


if __name__ == '__main__':
    unittest.main()
