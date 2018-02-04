import boto3
import time

client = boto3.resource('sqs',
                        endpoint_url='http://localhost:9324',
                        region_name='elasticmq',
                        aws_secret_access_key='x',
                        aws_access_key_id='x',
                        use_ssl=False)
sqs = boto3.client('sqs',
                   endpoint_url='http://localhost:9324',
                   region_name='elasticmq',
                   aws_secret_access_key='x',
                   aws_access_key_id='x',
                   use_ssl=False)


class Queu:
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
    for queue in client.queues.all():
        urls.append(Queu('XXX', queue.url,
                         queue.attributes.get('ApproximateNumberOfMessages'),
                         queue.attributes.get('ApproximateNumberOfMessagesNotVisible'),
                         queue.attributes.get('CreatedTimestamp')))
    return urls


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
