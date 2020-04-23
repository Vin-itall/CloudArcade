import time
from google.cloud import pubsub_v1
import googleapiclient.discovery

def listen():
    project_id = "cloudarcademaster-274423"
    subscription_name = "test"
    # timeout = 5.0  # "How long the subscriber should listen for messages in seconds"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        username = message.attributes.get('username')
        game = message.attributes.get('game')
        core = message.attributes.get('core')
        print(username, game, core)
        compute = googleapiclient.discovery.build('compute', 'v1')
        result = compute.instances().list(project='cloudarcademaster-274423', zone='us-west2-a', filter='status=TERMINATED').execute()
        instances = result['items'] if 'items' in result else None
        if instances:
            # print('DEKHO' + str(instances[0]['id']))

            # Start thread for this ID

            # Ack when IP is available
            message.ack()

    # Limit the subscriber to only have ten outstanding messages at a time.
    flow_control = pubsub_v1.types.FlowControl(max_messages=1)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback, flow_control=flow_control)
    print("Listening for messages on {}..\n".format(subscription_path))

    with subscriber:
        try:
            streaming_pull_future.result()
        except:  # empty
            streaming_pull_future.cancel()
