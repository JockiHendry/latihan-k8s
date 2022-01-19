import logging
import os
import uuid
from multiprocessing import Process
from pathlib import Path
from flask import Flask, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def create_app(test_publisher=None):
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
    publisher = test_publisher

    # create message queue processes
    app.logger.info('RabbitMQ enabled? %s', app.config['ENABLE_RABBITMQ'])
    if app.config['ENABLE_RABBITMQ']:
        from . import thumbnail_worker, publisher as publisher_module
        publisher = publisher_module.RabbitPublisher(rabbitmq_host, rabbitmq_port, rabbitmq_user, rabbitmq_password) \
            if publisher is None else publisher
        thumbnail_worker_process = Process(target=thumbnail_worker.setup,
                                           args=(rabbitmq_host, rabbitmq_port, rabbitmq_user, rabbitmq_password),
                                           daemon=True)
        thumbnail_worker_process.start()

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
            publisher.publish_file_uploaded({'filename': filename, 'folder': folder, 'filepath': filepath})\
                if publisher is not None else None
            return {'filename': filename}
        app.logger.error('Invalid filename %s', file.filename)
        return {'error': 'Invalid filename'}, 500

    @app.route('/health', methods=['GET'])
    def health():
        if thumbnail_worker_process.is_alive():
            return {'status': 'ok'}, 200
        return {'status': 'error'}, 500

    return app
