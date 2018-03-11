import boto3
import time

import configparser

config = configparser.ConfigParser()
config.sections()
config.read('./config/config.ini')
elastic = config['elasticmq']

params = {'endpoint_url': elastic['host'] + ':' + elastic['port'],
          'region_name': 'elasticmq',
          'aws_secret_access_key': elastic['aws_secret_access_key'],
          'aws_access_key_id': elastic['aws_access_key_id']}

client = boto3.resource('sqs',
                        endpoint_url=params['endpoint_url'],
                        region_name=params['region_name'],
                        aws_secret_access_key=params['aws_secret_access_key'],
                        aws_access_key_id=params['aws_access_key_id'],
                        use_ssl=False)
sqs = boto3.client('sqs',
                   endpoint_url=params['endpoint_url'],
                   region_name=params['region_name'],
                   aws_secret_access_key=params['aws_secret_access_key'],
                   aws_access_key_id=params['aws_access_key_id'],
                   use_ssl=False)

class Queue:
    def __init__(self, name, url, numMes, invisMes, tst):
        self.name = url.rsplit('/', 1)[-1]
        self.url = url
        self.numMes = numMes
        self.invisMes = invisMes
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(tst)))


class Message:
    def __init__(self, body, receiptHandle):
        self.body = body
        self.receiptHandle = receiptHandle


def cleint_get_queues():
    urls = []
    error = None
    try:
        for queue in client.queues.all():
            urls.append(Queue('XXX', queue.url,
                              queue.attributes.get('ApproximateNumberOfMessages'),
                              queue.attributes.get('ApproximateNumberOfMessagesNotVisible'),
                              queue.attributes.get('CreatedTimestamp')))

        def getKey(custom):
            return custom.name
        urls = sorted(urls, key=getKey)
    except Exception:
        error = "Cannot connect to "+ params['endpoint_url']
        return urls, error
    finally:
        return urls, error


def client_get_queu_by_name(name):
    return client.get_queue_by_name(QueueName=name)


def client_send_message(name, body):
    response = sqs.send_message(
        QueueUrl=client_get_queu_by_name(name).url,
        MessageBody=body
    )
    return response['MessageId']


def client_get_messages(name):
    result = []
    queue = client_get_queu_by_name(name)
    messages_count = queue.attributes['ApproximateNumberOfMessages']
    for i in range(int(messages_count)):
        messages = []
        messages = sqs.receive_message(QueueUrl=queue.url,
                                       MaxNumberOfMessages=10)
        if 'Messages' in messages:
            for message in messages['Messages']:
                result.append(Message(message['Body'], message['ReceiptHandle']))
        if len(messages) >= int(messages_count):
            break
    return result


def client_delete_message(name, receiptHandle):
    response = sqs.delete_message(QueueUrl=client_get_queu_by_name(name).url, ReceiptHandle=receiptHandle)
    return response


def client_purge(name):
    messages = client_get_messages(name)
    for i in range(len(messages)):
        client_delete_message(name, messages[i].receiptHandle)
