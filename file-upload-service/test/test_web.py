import unittest
import json
import shutil
from io import BytesIO
from pathlib import Path
from flask import Flask
from service import create_app
from multiprocessing import Queue


class WebTestCase(unittest.TestCase):

    def setUp(self):
        shutil.rmtree('/tmp/uploads', ignore_errors=True)
        Flask.env = 'testing'
        self.queue = Queue()
        self.app = create_app(self.queue)
        self.client = self.app.test_client()

    def test_upload(self):
        response = self.client.post('/upload', content_type='multipart/form-data',
                                    data={'file': (BytesIO(b'this is a sample file'), 'sample.txt')})
        self.assertEqual(response.status_code, 200)
        file1 = response.json['filename']
        self.assertIsNotNone(file1)
        self.assertTrue(Path('/tmp/uploads/{}'.format(file1)))
        self.assertTrue(file1.endswith('sample.txt'))
        response = self.client.post('/upload', content_type='multipart/form-data',
                                    data={'file': (BytesIO(b'this is a sample file'), 'sample.txt')})
        self.assertEqual(response.status_code, 200)
        file2 = response.json['filename']
        self.assertIsNotNone(file2)
        self.assertTrue(Path('/tmp/uploads/{}'.format(file2)))
        self.assertTrue(file2.endswith('sample.txt'))
        self.assertNotEqual(file1, file2)

    def test_upload_invalid_file(self):
        response = self.client.post('/upload', content_type='multipart/form-data',
                                    data={'file': (BytesIO(b'this is a sample file'), 'sample.exe')})
        self.assertEqual(response.status_code, 500)

    def test_publish_thumbnail_command_on_upload(self):
        response = self.client.post('/upload', content_type='multipart/form-data',
                                    data={'file': (BytesIO(b'this is a sample file'), 'sample.txt')})
        self.assertEqual(1, self.queue.qsize())
        self.assertDictEqual(json.loads(self.queue.get()), {
            'filename': response.json['filename'],
            'folder': '/tmp/uploads/',
            'filepath': '/tmp/uploads/{}'.format(response.json['filename'])
        })

    def test_upload_with_bucket(self):
        response = self.client.post('/bucket1/upload', content_type='multipart/form-data',
                                    data={'file': (BytesIO(b'this is a sample file'), 'sample.txt')})
        self.assertEqual(response.status_code, 200)
        file_name = response.json['filename']
        self.assertIsNotNone(file_name)
        self.assertTrue(Path('/tmp/uploads/bucket1/{}'.format(file_name)))
        self.assertTrue(file_name.endswith('sample.txt'))
        self.assertEqual(1, self.queue.qsize())
        self.assertDictEqual(json.loads(self.queue.get()), {
            'filename': file_name,
            'folder': '/tmp/uploads/bucket1',
            'filepath': '/tmp/uploads/bucket1/{}'.format(file_name)
        })


if __name__ == '__main__':
    unittest.main()
