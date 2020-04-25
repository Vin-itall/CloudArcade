# Start instance with given game and user
import boto3
import googleapiclient.discovery
from pprint import pprint
import time
import json

compute = googleapiclient.discovery.build('compute', 'v1')

def initiate(instance):

    sqs = boto3.client('sqs',region_name = 'us-east-1')
    key = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo')
    Receipt = key['Messages'][0]['ReceiptHandle']
    sqs.change_message_visibility(QueueUrl='https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo',
                       ReceiptHandle=Receipt, VisibilityTimeout = 10)
    message = key['Messages'][0]['Body']
    message = json.loads(message)

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
          }
         ]
    }

    try:
        request = compute.instances().setMetadata(project='cloudarcademaster-274423', zone='us-west3-a', instance=instance['name'], body=metadata_body)
        response = request.execute()

        if response:
            sqs.delete_message(QueueUrl = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo', ReceiptHandle = Receipt)
    except:
        print('Nhi ho paaya')

    request = compute.instances().start(project='cloudarcademaster-274423', zone='us-west3-a', instance=instance['name'])
    response = request.execute()

    # request = compute.instances().get(project='cloudarcademaster-274423', zone='us-west3-a', instance=instance)
    # response = request.execute()
    # pprint(response['metadata'])

if __name__ == '__main__':
    initiate('worker-1')
