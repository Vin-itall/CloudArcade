import boto3

queue_url = 'https://sqs.us-east-1.amazonaws.com/***************'
sqs = boto3.client('sqs', region_name='us-east-1')

messages = ['{"game": "barbie", "core": "snes", "username": "atmc"}',
    '{"game": "barbie", "core": "snes", "username": "demonz"}',
    '{"game": "barbie", "core": "snes", "username": "vampire"}',
    '{"game": "barbie", "core": "snes", "username": "cripz"}',
    '{"game": "barbie", "core": "snes", "username": "sattu"}'
]

for i, msg in enumerate(messages):
    sqs.send_message(QueueUrl=queue_url, MessageGroupId=str(i), MessageBody=msg)
