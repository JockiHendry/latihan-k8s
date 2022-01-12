import logging
import os
import uuid
import pika
import json
from pathlib import Path
from flask import Flask, request
from werkzeug.utils import secure_filename
from worker import worker_setup
from multiprocessing import Process

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
app = Flask(__name__)
app.config.from_object('config.{}Config'.format(app.env.title()))
rabbitmq_host = app.config['RABBITMQ_HOST']
rabbitmq_port = app.config['RABBITMQ_PORT']
rabbitmq_user = app.config['RABBITMQ_USER']
rabbitmq_password = app.config['RABBITMQ_PASSWORD']
upload_folder = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=pika.credentials.PlainCredentials(rabbitmq_user, rabbitmq_password),
    ))
channel = connection.channel()
channel.queue_declare('fileUploaded')
worker_process = Process(target=worker_setup, args=(rabbitmq_host, rabbitmq_port, rabbitmq_user, rabbitmq_password))
worker_process.start()


@app.route('/upload', methods=['POST'])
@app.route('/<folder>/upload', methods=['POST'])
def upload(folder=None):
    app.logger.info('Handling new file upload: %s', request.files)
    if 'file' not in request.files:
        app.logger.error('file not found in request')
        return {'error': 'Can\'t find file to upload'}, 400
    file = request.files['file']
    if file.filename == '':
        app.logger.error('filename not found')
        return {'error': 'Can\'t find file to upload'}, 400
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = '{}-{}' .format(uuid.uuid4(), secure_filename(file.filename))
        folder = os.path.join(upload_folder, secure_filename(folder) if folder is not None else '')
        app.logger.info('Create folder %s if necessary', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join(folder, filename)
        app.logger.info('Storing new file %s', filepath)
        file.save(filepath)
        app.logger.info('File %s stored', filename)
        channel.basic_publish(
            exchange='',
            routing_key='fileUploaded',
            body=json.dumps({'filename': filename, 'folder': folder, 'filepath': filepath}).encode('utf-8'))
        app.logger.info('fileUploaded message sent')
        return {'filename': filename}
    app.logger.error('Invalid filename %s', file.filename)
    return {'error': 'Invalid filename'}, 500


if __name__ == '__main__':
    app.run()
