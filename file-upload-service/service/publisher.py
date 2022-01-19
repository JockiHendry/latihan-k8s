import pika
import logging
import json


class RabbitPublisher:

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.credential = pika.credentials.PlainCredentials(user, password)
        self.connection = None
        self.channel = None

    def create_connection(self):
        logging.info('Creating new connection')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=self.credential,
        ))
        channel = connection.channel()
        channel.queue_declare('fileUploaded')
        self.connection = connection
        self.channel = channel

    def is_connection_valid(self):
        return (self.connection is not None and self.connection.is_open) and \
               (self.channel is not None and self.channel.is_open)

    def publish_file_uploaded(self, message):
        logging.info('Publishing fileUploaded message: %s', message)
        if not self.is_connection_valid():
            self.create_connection()
        while True:
            try:
                self.channel.basic_publish(exchange='', routing_key='fileUploaded',
                                           body=json.dumps(message).encode('utf-8'))
                break
            except pika.exceptions.AMQPChannelError as err:
                logging.error('Channel error: %s', err)
                break
            except pika.exceptions.AMQPConnectionError as err:
                logging.error('Connection error: %s', err)
                self.create_connection()
                continue
