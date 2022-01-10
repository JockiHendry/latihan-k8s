import os
import uuid
import logging
from pathlib import Path

from flask import Flask, request
from werkzeug.utils import secure_filename

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50_000_000

ALLOWED_EXTENSIONS = {'txt', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', default='/uploads')
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload():
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
        app.logger.info('Storing new file %s', filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        app.logger.info('File {} stored', filename)
        return {'filename': filename}
    app.logger.error('Invalid filename %s', file.filename)
    return {'error': 'Invalid filename'}, 500


if __name__ == '__main__':
    app.run()
