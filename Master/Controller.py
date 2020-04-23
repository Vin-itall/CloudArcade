from flask import Flask, render_template, Response, request
from google.cloud import pubsub_v1
import time
import threading
import Listener

Controller = Flask(__name__)

project_id = "cloudarcademaster-274423"
topic_name = "loginqueue"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

thread = None

def publish_message(username, game):
    future = publisher.publish(topic_path, b'', username=username, game=game)
    print('Successfully uploaded' + str(future.result()))

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
    game = request.args.get('game')
    publish_message(username, game)
    return ('Loading...')

if __name__ == '__main__':
    Controller.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
