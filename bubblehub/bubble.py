import json
import config


class Bubble:

    def __init__(self, bubble_id, channel):
        self.bubble_id = bubble_id
        self.channel = channel
        # create the incoming game exchange/queue
        self.channel.exchange_declare(exchange=config.GAME_IN_EXCHANGE, exchange_type="topic")
        result = self.channel.queue_declare('', exclusive=True)
        self.queue_in_name = result.method.queue
        self.channel.basic_consume(queue=self.queue_in_name, on_message_callback=self.on_game_message, auto_ack=True)
        self.game_id = 'unknown'
        # create the outgoing exchange
        self.channel.exchange_declare(exchange=config.GAME_OUT_EXCHANGE, exchange_type="topic")

    def start_game(self, game_id):
        self.game_id = game_id
        self.channel.queue_bind(
            exchange=config.GAME_IN_EXCHANGE,
            queue=self.queue_in_name,
            routing_key=self.game_id
        )
        reply = {
            'cmd': "starting",
            'bubble': self.bubble_id,
            'game': self.game_id
        }
        j = json.dumps(reply)
        self.channel.basic_publish(exchange=config.GAME_OUT_EXCHANGE,
                                   routing_key=config.GAME_STATUS_QUEUE,
                                   body=j)

    def stop_game(self):
        self.channel.queue_unbind(
            exchange=config.GAME_IN_EXCHANGE,
            queue=self.queue_in_name,
            routing_key=self.game_id
        )

    def on_game_message(self, ch, method, props, body):
        print(f"game message: {body}")
