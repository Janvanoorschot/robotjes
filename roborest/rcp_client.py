import uuid
import json
import pika


class RPCClient:

    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.callback_queue = None
        self.correlation_id = None
        self.callback = None

    def connect(self, channel):
        self.channel = channel
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            try:
                reply = json.loads(body)
            except json.JSONDecodeError as jde:
                pass
            self.callback(reply)

    def call(self, message, cb):
        self.callback = cb
        try:
            body = json.dumps(message)
        except:
            pass
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=body)
