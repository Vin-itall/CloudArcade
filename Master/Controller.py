from flask import Flask, render_template, Response, request, redirect
import time
import threading
import Listener
import boto3
from pprint import pprint

Controller = Flask(__name__)

queue_url = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/067610562392/responseQueue.fifo'
sqs = boto3.client(
    'sqs',
    'us-east-1',
    aws_access_key_id= AWS_CREDENTIALS.aws_access_key_id,
    aws_secret_access_key= AWS_CREDENTIALS.aws_secret_access_key
    # aws_session_token=SESSION_TOKEN,
)

thread = None

def checkResponseQueueSize():
    QSize = sqs.get_queue_attributes(
            QueueUrl=response_queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
    QSize = QSize['Attributes']['ApproximateNumberOfMessages']
    return int(QSize)

def publish_message(username, game, core):
    MessageAttributes = '{"game": "' + str(game)  + '","core": "' + str(core) + '","username": "' + str(username) + '"}'
    sqs.send_message(QueueUrl=queue_url, MessageGroupId=username, MessageBody=MessageAttributes)
    print('Successfully uploaded to Service queue')

def listen_response(username):
    sqs = boto3.client('sqs', region_name='us-east-1')
    redirect_ip = None
    while True:
        print('Waiting for streaming server to start for ' + username)

        if checkResponseQueueSize() > 0:
            print('Receiving messages')
            key = sqs.receive_message(QueueUrl=response_queue_url)
            for msg in key['Messages']:
                pprint(msg)
                if msg['Body'].split('/')[-1] == username:
                    redirect_ip = msg['Body']
                    sqs.delete_message(QueueUrl = response_queue_url, ReceiptHandle = msg['ReceiptHandle'])
                    break

        if redirect_ip:
            break

        time.sleep(10)

    # Redirect to that user's server
    print('Redirecting for ' + username)
    return redirect_ip

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
    redirect_ip = listen_response(username)
    return redirect(redirect_ip)

if __name__ == '__main__':
    Controller.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
