from locale import currency
from flask import Blueprint, render_template, request, redirect, url_for
from website import views
from pymongo import MongoClient
import time
#from website.consume import consume_que_msg

from website.models import Feedback, User, Result
from website.publish import publish_result
from website.publish_f import publish_feedback
from . import db, create_app
import pika
# from threading import Thread



auth = Blueprint('auth', __name__)
@auth.route('/signin/', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        roll = request.form.get('roll')
        password = request.form.get('password')
        user = User.query.filter_by(roll=roll).first()
        if user:
            if user.password == password:
                return redirect(url_for('auth.dash', roll=roll))

    return render_template("signin.html")

@auth.route('/signup/',  methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        roll = request.form.get('roll')
        section = request.form.get('section')
        password = request.form.get('password')

        new_user =  User(roll=roll, section=section, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.home'))
    

    return render_template("signup.html")

@auth.route('/produce/', methods=['GET','POST'])
def produce():
    cluster = "mongodb://localhost:27017"
    client = MongoClient(cluster)
    db = client.NEW_DB
    print(db.list_collection_names())
    t = db.textFles
    r = t.find_one({"File_2": 3714060})
    if r:
        print("yes")
    else:
        print("no")
    if request.method == 'POST':
        roll = request.form.get('roll')
        result = request.form.get('result')

        publish_result(result=result,roll=roll)

    feeds = Feedback.query.filter().all()
    return render_template("pro.html", feeds = feeds)


@auth.route('/dash/', methods=['GET','POST'])
def dash():
    def consume_que_msg():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        msg_num = channel.queue_declare(queue="message").method.message_count
        if msg_num:
            for method, properties, body in channel.consume('message'):
                msg = body.decode('utf-8')
                l = msg.split(';')
                #print(" [x] Received %r" % l)
                roll = request.args.get('roll')
                if l[0] == roll:
                    channel.basic_ack(method.delivery_tag)
                    new_result = Result(result=l[1], roll=l[0])
                    db.session.add(new_result)
                    db.session.commit()
                    break
                elif msg_num == method.delivery_tag:
                    break

            channel.cancel()
            channel.close()
            connection.close()

    #print("dashboard start")
    consume_que_msg()
    #print("dashboard continue")
    
    roll = request.args.get('roll')
    result = Result.query.filter_by(roll=roll).first()
    curr_res = ""
    if result:
        curr_res = result.result

    if request.method == 'POST':
        roll = request.form.get('roll')
        feedback = request.form.get('feedback')
        publish_feedback(roll=roll,feedback=feedback)
    return render_template("dash.html", roll = roll , res = curr_res)



