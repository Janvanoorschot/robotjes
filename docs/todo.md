# Working on Bubble queueing protocol

A bubble listens to the following queues:

* bubblehubqueue: Rest_Server talking to BubbleHub
* bubblesqueue: BubbleHub talking to Bubbles
* gamesqueue: REST server talking to Bubbles

options for 'busy' Bubble;
1. Let the Bubble disconnect from queue
2. Let the Bubble 'nack' requests when it is busy
3. Let the Bubble not send a n 'ack'

It seems that long running jobs should be scheduled with 'ack' only send it when really done. 
However, the longrunning job should run in a seperate thread. Check the following [example
from the pika repot](https://github.com/pika/pika/blob/0.12.0/examples/basic_consumer_threaded.py).

remove the alternative channel from code
* upgrade bubble_hub so it uses its own exchange
* upgrade bubble so it uses the same exchange
* start the Bubble on its own thread
* let the Bubble attach to the games_in_queue
* let the Bubble attach to the games_out_queue


https://github.com/vitaly-krugl/pika/blob/94f86187bf8cbd6cdc18a52f17c564fbb2c78169/tests/acceptance/blocking_adapter_test.py#L1550-L1649