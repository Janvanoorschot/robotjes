from robotjessrv import config
# pika var
pikaurl = None

# fastapi vars
app = None
async_rpc_client = None
async_topic_listener = None
async_field_listener = None

#
status_keeper = None

# aio_pika vars
connection = None
channel = None
games_exchange_name = config.GAMES_EXCHANGE
games_exchange = None

