import config

# pika var
pikaurl = None
# fastapi vars
app = None
async_rpc_client = None
# aio_pika vars
connection = None
channel = None
games_exchange_name = config.GAMES_EXCHANGE
games_exchange = None
