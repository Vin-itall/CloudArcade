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
    result = compute.instances().list(project='cloudarcademaster-274423', zone='us-west2-a', filter='status=TERMINATED').execute()
    instances = result['items'] if 'items' in result else None

    return instances

def listen():
    sqs = boto3.client('sqs', region_name='us-east-1')
    Queue = 'https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo'

    while True:
        qSize = int(checkQueueSize())
        instances = getTerminatedInstances()
        numTerminated = len(instances) if instances else 0
        numToStart = min(qSize, numTerminated)
        # print(numTerminated)

        for i in range(numToStart):
            instance = instances[i]

            thread = threading.Thread(target=InitiateWorker.initiate, args=(instance, ))
            thread.start()

        time.sleep(10)

if __name__ == '__main__':
    listen()
