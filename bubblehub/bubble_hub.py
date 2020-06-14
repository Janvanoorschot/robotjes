import json
import pika
import logging
logger = logging.getLogger(__name__)
import config

from bubblehub.model import BubbleSpec, ConnectionSpec, BubbleStatus

class BubbleHub:

    def __init__(self):
        self.bubblehubs_exchange_name = config.BUBBLEHUBS_EXCHANGE
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.bubblehubs_queue_name = config.BUBBLEHUBS_QUEUE
        self.gamestatus_queue_name = config.GAME_STATUS_QUEUE

    def connect(self, channel):
        self.channel = channel
        # create exchange/queue to and from the rest-server (we are in the consumer role)
        self.channel.exchange_declare(exchange=self.bubblehubs_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubblehubs_queue_name)
        self.channel.queue_bind(queue=self.bubblehubs_queue_name, exchange=self.bubblehubs_exchange_name)
        self.channel.basic_consume(queue=self.bubblehubs_queue_name, on_message_callback=self.on_rest_request)
        # create exchange/queue to and from the bubbles (we are in the producers role)
        self.channel.exchange_declare(exchange=self.bubbles_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubbles_queue_name)
        self.channel.queue_bind(queue=self.bubbles_queue_name, exchange=self.bubbles_exchange_name)
        # create exchange/queue to and from the games (run by bubbles) (we are in the consumer role)
        self.channel.exchange_declare(exchange=self.games_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubbles_queue_name)
        self.channel.queue_bind(queue=self.bubbles_queue_name, exchange=self.games_exchange_name)
        self.channel.basic_consume(queue=self.bubbles_queue_name, on_message_callback=self.on_game_status)

    def on_rest_request(self, ch, method, props, body):
        logger.warning("on_rest_request")
        """ do the request/run/reply cycle"""
        try:
            request = json.loads(body)
            cmd = request.get('cmd', 'unknown')
            if cmd == 'create_bubble':
                specs = request.get('specs', None)
                self.create_bubble(BubbleSpec.parse_obj(specs))
                reply = {'success': True}
            else:
                reply = {'success': False, 'error': f"unknown command: {cmd}"}
        except json.decoder.JSONDecodeError as jsonerror:
            reply = {'success': False, 'error': str(jsonerror)}
        except Exception as e:
            reply = {'success': False, 'error': str(e)}
        # send back an error-reply over 'reply_to' queue
        j = json.dumps(reply)
        ch.basic_publish(exchange=self.bubblehubs_exchange_name,
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = props.correlation_id),
                         body=j)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def on_game_status(self, ch, method, props, body):
        logger.warning("on_game_status")
        pass

    def create_bubble(self, specs: BubbleSpec):
        body = json.dumps(specs.dict())
        self.channel.basic_publish(exchange=self.bubbles_exchange_name,
                             routing_key=self.bubbles_queue_name,
                             body=body)

