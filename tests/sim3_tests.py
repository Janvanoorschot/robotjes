import json
import pika
import uuid
import unittest
import os

from robotjes.remote import Handler
from robotjes.sim import Engine, Map

DIR = os.path.dirname(os.path.abspath(__file__))


class Sim3TestCase(unittest.TestCase):
    """ Test the Pika connection to our simulation """

    def setUp(self):
        self.rmqhost = 'localhost'
        self.rmqport = 5672
        self.rmqqueue = 'rpc_queue'
        self.response = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rmqhost, port=self.rmqport))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue,on_message_callback=self.on_response, auto_ack=True)

    def tearDown(self):
        pass

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, request):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.rmqqueue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(request))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def go(self, map_file, success_file, script_file):
        map_path = os.path.join(DIR, os.pardir, 'tests/datafiles', map_file)
        success_path = os.path.join(DIR, os.pardir, 'tests/datafiles', success_file)
        script_path = os.path.join(DIR, os.pardir, 'tests/datafiles', script_file)
        with open(map_path, 'r') as f:
            map = f.read()
        with open(success_path, 'r') as f:
            success = json.loads(f.read())
        with open(script_path, 'r') as f:
            script = f.read()
        request = {
            "map": map,
            "success": success,
            "script": script
        }
        response = self.call(request)
        return response

    def test_sim301(self):
        response = self.go("sim3.map", "sim3.json", "sim301.py")
        self.assertIsNotNone(response)

    def test_sim302(self):
        response = self.go("sim3.map", "sim3.json", "sim302.py")
        self.assertIsNotNone(response)

    def test_sim303(self):
        response = self.go("sim3.map", "sim3.json", "sim303.py")
        self.assertIsNotNone(response)

    def test_sim304(self):
        response = self.go("sim3.map", "sim3.json", "sim304.py")
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
