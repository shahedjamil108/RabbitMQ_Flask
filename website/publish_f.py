
import pika
import os 
def publish_feedback(roll, feedback):
    print(roll)
    msg = roll + ';'+feedback;
    print(f" [x] Sending '{msg}'")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='feedback')

    channel.basic_publish(exchange='', routing_key='feedback', body=msg)
    print(f" [x] Sent '{msg}'")
    connection.close()