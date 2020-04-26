import time
import boto3
import googleapiclient.discovery
from pprint import pprint
import threading
import InitiateWorker

sqs = boto3.client('sqs', region_name='us-east-1')
Queue = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo'
compute = googleapiclient.discovery.build('compute', 'v1')
thread = None

def checkQueueSize():
    QSize = sqs.get_queue_attributes(
            QueueUrl=Queue,
            AttributeNames=['ApproximateNumberOfMessages']
        )
    QSize = QSize['Attributes']['ApproximateNumberOfMessages']
    return QSize

def getTerminatedInstances():
    result = compute.instances().list(project='cloudarcademaster-274423', zone='us-west3-a', filter='status=TERMINATED').execute()
    instances = result['items'] if 'items' in result else None
    returnable = instances
    # for item in instances:
    #     if item['status']== "TERMINATED":
    #         returnable.append(item)
    return returnable

def listen():
    sqs = boto3.client('sqs', region_name='us-east-1')
    Queue = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo'
    while True:
        print('Checking service queue for new message...')
        qSize = int(checkQueueSize())
        instances = getTerminatedInstances()
        numTerminated = len(instances) if instances else 0
        print('Queue Size:'+str(qSize))
        print('Num Terminated:'+str(numTerminated))
        numToStart = min(qSize, numTerminated)
        print('Starting no. of workers ='+str(numToStart))
        for i in range(numToStart):
            instance = instances[i]
            InitiateWorker.initiate(instance)

        time.sleep(10)

if __name__ == '__main__':
    listen()
