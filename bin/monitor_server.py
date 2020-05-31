#!/usr/bin/env python3

import pika
import json
import sys, os
import argparse
from sqlalchemy import create_engine
from monitor import MonitorServer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
MONITOR_EXCHANGE = "monitor_exchange"
DBASE_USER = "rmprod"
DBASE_PWD = "rmprodsecret"
DBASE_HOST = "localhost"
DBASE_PORT = 5432
DBASE_NAME = "monitor"

# get commandline arguments
parser = argparse.ArgumentParser(description='Start the Monitor Server.')
parser.add_argument('--pikaurl', type=str, default=PIKA_URL, help='pika url')
parser.add_argument('--monitorexchange', type=str, default=MONITOR_EXCHANGE, help='monitor exchange')

parser.add_argument('--dbuser', type=str, default=DBASE_USER, help='database user')
parser.add_argument('--dbpwd', type=str, default=DBASE_PWD, help='database password')
parser.add_argument('--dbhost', type=str, default=DBASE_HOST, help='database host')
parser.add_argument('--dbport', type=str, default=DBASE_PORT, help='database port')
parser.add_argument('--dbname', type=str, default=DBASE_NAME, help='database name')

args = parser.parse_args()

# connect to the database
# connection string: postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
dbconstr = f"postgresql+psycopg2://{args.dbuser}:{args.dbpwd}@{args.dbhost}:{args.dbport}/{args.dbname}"
engine = create_engine(dbconstr, echo=False)
from monitor.model import Base

# recreate the database tables ... not for production
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# create our monitor-server object
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
monitor_server = MonitorServer(Session())

def on_request(ch, method, props, body):
    """ do the request/run/reply cycle"""
    try:
        request = json.loads(body)
        monitor_server.handle(request)
    except json.decoder.JSONDecodeError as jsonerror:
        msg = {}
        msg['type'] = 'jsonerror'
        msg['message'] = str(jsonerror)
        monitor_server.handle(msg)
    except Exception as e:
        msg = {}
        msg['type'] = 'exception'
        msg['message'] = str(e)
        monitor_server.handle(msg)

# prepare pika (blocking, one RPC queue and a requestor-created reply-to queue)
parameters = pika.URLParameters(args.pikaurl)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange=args.monitorexchange, exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True, )
queue_name = result.method.queue
channel.queue_bind(exchange=args.monitorexchange, queue=queue_name)

# start listening for work
channel.basic_consume(queue=queue_name, on_message_callback=on_request, auto_ack=True)
channel.start_consuming()
