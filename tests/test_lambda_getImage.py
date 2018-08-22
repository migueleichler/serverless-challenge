import unittest
from moto import mock_s3
from tests.set_up import set_up_s3
from handler import getImage
import os


class TestLambdaGetImage(unittest.TestCase):

    def setUp(self):
        self.bucket = 'teste'
        self.s3objectkey = 'image-001'
        self.file_path = os.path.dirname(os.path.abspath(__file__)) + '/tmp/'
        self.file_name = self.file_path + 'image.png'

        self.event = {
            "queryStringParameters": [
                {
                    "s3objectkey": self.s3objectkey,
                }
            ]
        }

    @mock_s3
    def test_getImage(self):
        s3 = set_up_s3(
                 bucket=self.bucket,
                 s3objectkey=self.s3objectkey,
                 file_name=self.file_name
             )

        getImage(self.event, None)

    def tearDown(self):
        os.remove(self.file_name)
