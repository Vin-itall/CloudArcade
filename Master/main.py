from flask import Flask, render_template, Response, request, redirect
import time
import threading
import Listener
import boto3
from pprint import pprint
import AWS_CREDENTIALS
import sys

app = Flask(__name__)

queue_url = 'https://sqs.us-east-1.amazonaws.com/**********************'
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/************************'
sqs = boto3.client(
    'sqs',
    'us-east-1',
    aws_access_key_id = '*******************',
    aws_secret_access_key= '*******************************'
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
    redirect_ip = None
    while True:
        print('Waiting for streaming server to start for ' + username)

        if checkResponseQueueSize() > 0:
            print('Receiving messages')
            key = sqs.receive_message(QueueUrl=response_queue_url)
            try:
                if 'Messages' in key:
                    for msg in key['Messages']:
                        print(msg['Body'].split('/')[-1], username)
                        if msg['Body'].split('/')[-1] == username:

                            redirect_ip = msg['Body']
                            print(redirect_ip)
                            sqs.delete_message(QueueUrl = response_queue_url, ReceiptHandle = msg['ReceiptHandle'])
                            # Redirect to that user's server
                            print('Redirecting for ' + username)
                            return redirect_ip

            except:
                print(checkResponseQueueSize())
                print(sys.exc_info())

        time.sleep(10)


@app.route('/')
def index():
    global thread
    if not thread:
        thread = threading.Thread(target=Listener.listen)
        thread.start()
    return render_template('MainPage.html')

@app.route('/login_action')
def login():
    username = request.args.get('username')
    core = request.args.get('core')
    game = request.args.get('game')

    publish_message(username, game, core)
    ip = listen_response(username)
    print(ip)
    return redirect(ip)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
