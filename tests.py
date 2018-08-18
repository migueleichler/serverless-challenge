import unittest
import boto3
from moto import mock_s3
from handler import extractMetadata


class TestHandlerFunctions(unittest.TestCase):

    @mock_s3
    def setUp(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='teste')

        self.event = {}

    def test_extractMetadata(self):
        extractMetadata(self.event, None)
