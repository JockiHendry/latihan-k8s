import json
import logging
import pika
import subprocess
import os
from pathlib import Path

logger = logging.getLogger(__name__)
ALLOWED_IMAGES = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}


def on_file_uploaded(_ch, _method, _properties, body):
    message = json.loads(body)
    logger.info('Receiving message: %s', message)
    if message['filename'].rsplit('.', 1)[1].lower() in ALLOWED_IMAGES:
        thumbnail_folder = os.path.join(message['folder'], 'thumbnail')
        Path(thumbnail_folder).mkdir(parents=True, exist_ok=True)
        thumbnail_file = os.path.join(thumbnail_folder, message['filename'])
        subprocess.call(['convert', message['filepath'], '-thumbnail', '200x200>', thumbnail_file])
        logger.info('Thumbnail created: %s', thumbnail_file)


def worker_setup(host, port, user, password):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=pika.credentials.PlainCredentials(user, password),
    ))
    channel = connection.channel()
    channel.queue_declare('fileUploaded')
    channel.basic_consume('fileUploaded', on_file_uploaded, auto_ack=True)
    channel.start_consuming()
