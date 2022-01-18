import logging
import uuid
import json
import os
from pathlib import Path
from flask import Flask, request
from multiprocessing import Process, Queue
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
thumbnail_command_queue = Queue()


def create_app(command_queue=None):
    # create Flask app
    app = Flask(__name__)
    config_string = 'service.config.{}Config'.format(app.env.title())
    app.logger.info('Reading config from %s', config_string)
    app.config.from_object(config_string)
    rabbitmq_host = app.config['RABBITMQ_HOST']
    rabbitmq_port = app.config['RABBITMQ_PORT']
    rabbitmq_user = app.config['RABBITMQ_USER']
    rabbitmq_password = app.config['RABBITMQ_PASSWORD']
    upload_folder = app.config['UPLOAD_FOLDER']
    command_queue = thumbnail_command_queue if command_queue is None else command_queue

    # create message queue processes
    app.logger.info('RabbitMQ enabled? %s', app.config['ENABLE_RABBITMQ'])
    if app.config['ENABLE_RABBITMQ']:
        from . import thumbnail_queue, thumbnail_worker
        thumbnail_worker_process = Process(target=thumbnail_worker.setup,
                                           args=(rabbitmq_host, rabbitmq_port, rabbitmq_user, rabbitmq_password),
                                           daemon=True)
        thumbnail_worker_process.start()
        thumbnail_queue_process = Process(target=thumbnail_queue.setup,
                                          args=(rabbitmq_host, rabbitmq_port, rabbitmq_user, rabbitmq_password,
                                                command_queue), daemon=True)
        thumbnail_queue_process.start()

    # routes

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
            filename = '{}-{}'.format(uuid.uuid4(), secure_filename(file.filename))
            folder = os.path.join(upload_folder, secure_filename(folder) if folder is not None else '')
            app.logger.info('Create folder %s if necessary', folder)
            Path(folder).mkdir(parents=True, exist_ok=True)
            filepath = os.path.join(folder, filename)
            app.logger.info('Storing new file %s', filepath)
            file.save(filepath)
            app.logger.info('File %s stored', filename)
            command_queue.put(json.dumps({'filename': filename, 'folder': folder, 'filepath': filepath})
                                        .encode('utf-8'))
            return {'filename': filename}
        app.logger.error('Invalid filename %s', file.filename)
        return {'error': 'Invalid filename'}, 500

    @app.route('/health', methods=['GET'])
    def health():
        if thumbnail_worker_process.is_alive() and thumbnail_queue_process.is_alive():
            return {'status': 'ok'}, 200
        return {'status': 'error'}, 500

    return app
