import pika
import os
from website.models import Feedback
from . import db, create_app 


app = create_app()

def got_msg(ch, method, properties, body):
    msg = body.decode('utf-8')

    l = msg.split(';')

    with app.app_context():
        new_feedback = Feedback(roll=l[0], feedback=l[1])
        db.session.add(new_feedback)
        db.session.commit()
        print(" [x] Received %r" % l)


def consume_feed():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue="feedback")

    channel.basic_consume(
        queue="feedback",
        auto_ack=True,
        on_message_callback=got_msg
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()