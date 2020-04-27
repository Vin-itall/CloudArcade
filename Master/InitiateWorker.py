# Start instance with given game and user
import boto3
import googleapiclient.discovery
from pprint import pprint
import time
import json
import AWS_CREDENTIALS

compute = googleapiclient.discovery.build('compute', 'v1')

def initiate(instance):
    print('Starting new worker ' + instance['name'])
    sqs = boto3.client(
        'sqs',
        'us-east-1',
        aws_access_key_id= AWS_CREDENTIALS.aws_access_key_id,
        aws_secret_access_key= AWS_CREDENTIALS.aws_secret_access_key
        # aws_session_token=SESSION_TOKEN,
    )
    key = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo')
    Receipt = key['Messages'][0]['ReceiptHandle']
    sqs.change_message_visibility(QueueUrl='https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo',
                       ReceiptHandle=Receipt, VisibilityTimeout = 100)
    message = key['Messages'][0]['Body']
    message = json.loads(message)
    print('Message loaded')

    metadata_body = {
         "fingerprint": instance['metadata']['fingerprint'],
         "items": [
          {
           "key": "username",
           "value": message['username']
          },
          {
           "key": "core",
           "value": message['core']
          },
          {
           "key": "game",
           "value": message['game']
          },
          {
           "key": "startup-script",
           "value": '''#! /bin/bash
            pip3 install pygame flask boto3 pillow
            pip3 install google-api-python-client
            apt install python3-pyaudio
            cd /home/vjachary/CloudArcade/Worker/
            python3 /home/vjachary/CloudArcade/Worker/StreamingServer.py'''
          }
         ]
    }

    try:
        request = compute.instances().setMetadata(project='cloudarcademaster-274423', zone='us-west3-a', instance=instance['name'], body=metadata_body)
        response = request.execute()
        print('Metadata Set')

        if response:
            sqs.delete_message(QueueUrl = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo', ReceiptHandle = Receipt)
    except:
        print('Nhi ho paaya')

    request = compute.instances().start(project='cloudarcademaster-274423', zone='us-west3-a', instance=instance['name'])
    response = request.execute()

    print('New Worker started for user ' + message['username'])
    # request = compute.instances().get(project='cloudarcademaster-274423', zone='us-west3-a', instance=instance)
    # response = request.execute()
    # pprint(response['metadata'])

if __name__ == '__main__':
    initiate('worker-1')
