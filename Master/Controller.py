from flask import Flask, render_template, Response, request
import time
import threading
import Listener
import boto3

Controller = Flask(__name__)

queue_url = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo'
sqs = boto3.client('sqs', region_name='us-east-1')

thread = None

def publish_message(username, game, core):
    MessageAttributes = '{"game": "' + str(game)  + '","core": "' + str(core) + '","username": "' + str(username) + '"}'
    sqs.send_message(QueueUrl=queue_url, MessageGroupId=username, MessageBody=MessageAttributes)
    print('Successfully uploaded')

@Controller.route('/')
def index():
    global thread
    if not thread:
        thread = threading.Thread(target=Listener.listen)
        thread.start()
    return render_template('MainPage.html')

@Controller.route('/login_action')
def login():
    username = request.args.get('username')
    core = request.args.get('core')
    game = request.args.get('game')

    publish_message(username, game, core)
    return ('Loading...')

if __name__ == '__main__':
    Controller.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
