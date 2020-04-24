# Start instance with given game and user
import boto3

def initiate(instance):
    # request = compute.instances().start(project='cloudarcademaster-274423', zone='us-west2-a', instance=instance)
    # response = request.execute()
    # pprint(response)
    sqs = boto3.client('sqs',region_name = 'us-east-1')
    key = sqs.receive_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo')
    Receipt = key['Messages'][0]['ReceiptHandle']
    sqs.change_message_visibility(QueueUrl='https://sqs.us-east-1.amazonaws.com/067610562392/serviceFifo.fifo',
                       ReceiptHandle=Receipt, VisibilityTimeout = 200)
    print(key['Messages'][0]['Body'])
    # print(instance['name'])
