import boto3

sqs = boto3.client('sqs', region_name='us-east-1')

Queue = 'https://sqs.us-east-1.amazonaws.com/***********************'
def checkQueueSize():
    QSize = sqs.get_queue_attributes(
            QueueUrl=Queue,
            AttributeNames=['ApproximateNumberOfMessages']
        )
    QSize = QSize['Attributes']['ApproximateNumberOfMessages']
    return QSize

if __name__ == '__main__':
    l = checkQueueSize()
    print(l)
