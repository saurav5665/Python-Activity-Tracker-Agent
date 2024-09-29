import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uploader import S3Uploader

class TestS3Uploader(unittest.TestCase):

    @patch('uploader.boto3.client')
    def setUp(self, mock_boto_client):
        self.mock_s3 = mock_boto_client.return_value
        self.uploader = S3Uploader('fake_access_key', 'fake_secret_key', 'fake_bucket')

    @patch('uploader.os.path.isfile', return_value=True)
    def test_upload_file_success(self, mock_isfile):
        result = self.uploader.upload_file('fake_file_path')
        self.assertTrue(result)
        self.mock_s3.upload_file.assert_called_with('fake_file_path', 'fake_bucket', 'fake_file_path')

    @patch('uploader.os.path.isfile', return_value=False)
    def test_upload_file_failure(self, mock_isfile):
        result = self.uploader.upload_file('non_existent_file')
        self.assertFalse(result)

    @patch('uploader.boto3.client')
    def test_upload_file_securely(self, mock_boto_client):
        mock_s3_client = mock_boto_client.return_value
        mock_s3_client.upload_file.side_effect = MagicMock()

        result = self.uploader.upload_file_securely("fake_file_path")
        self.assertTrue(result)
        mock_s3_client.upload_file.assert_called_with(
            "fake_file_path", "fake_bucket", "fake_file_path", ExtraArgs={'ServerSideEncryption': 'AES256'}
        )

if __name__ == '__main__':
    unittest.main()
