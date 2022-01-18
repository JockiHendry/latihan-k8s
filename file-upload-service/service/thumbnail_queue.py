import pika
import logging
from queue import Empty

logger = logging.getLogger(__name__)


def setup(host, port, user, password, queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=pika.credentials.PlainCredentials(user, password),
    ))
    channel = connection.channel()
    channel.queue_declare('fileUploaded')
    while True:
        try:
            command = queue.get(block=False)
            logger.info('Receiving fileUploaded command: %s', command)
            channel.basic_publish(exchange='', routing_key='fileUploaded', body=command)
        except Empty:
            pass
        finally:
            connection.sleep(10)

