
import pika
from dotenv import load_dotenv
import os, sys 
load_dotenv()

#connection_url = os.environ.get('connection_url')

def publish_result(result, roll):
    msg = roll + ';' + result;
    print(f" [x] Sending '{msg}'")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='message')

    channel.basic_publish(exchange='', routing_key='message', body=msg)
    print(f" [x] Sent '{msg}'")
    connection.close()