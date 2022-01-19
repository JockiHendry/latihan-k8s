import json
import shutil
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from service.thumbnail_worker import on_file_uploaded


class WebTestCase(unittest.TestCase):

    def setUp(self):
        shutil.rmtree('/tmp/uploads/test', ignore_errors=True)

    def test_create_thumbnail(self):
        channel_mock = Mock()
        method_mock = Mock(delivery_tag=1)
        call = Mock()
        body = json.dumps({'filename': 'image.png', 'folder': '/tmp/uploads/test',
                           'filepath': '/tmp/uploads/test/img.png'})
        with patch('subprocess.call', new=call):
            on_file_uploaded(channel_mock, method_mock, None, body)
            channel_mock.basic_ack.assert_called_once()
            self.assertTrue(Path('/tmp/uploads/test').exists())
        call.assert_called_once_with(['convert', '/tmp/uploads/test/img.png', '-thumbnail',
                                      '200x200>', '/tmp/uploads/test/thumbnail/image.png'])
        channel_mock.basic_ack.assert_called_once_with(method_mock.delivery_tag)


if __name__ == '__main__':
    unittest.main()
