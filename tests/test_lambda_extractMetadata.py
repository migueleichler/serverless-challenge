import unittest
from moto import mock_s3, mock_dynamodb2
from handler import extractMetadata
from tests.set_up import set_up_dynamodb_client, set_up_s3
import os


class TestLambdaExtractMetadata(unittest.TestCase):

    def setUp(self):
        self.bucket = 'teste'
        self.s3objectkey = 'image-001'
        self.table = 'images'
        self.file_path = os.path.dirname(os.path.abspath(__file__)) + '/tmp/'
        self.file_name = self.file_path + 'image.png'

        self.event = {
            "Records": [
                {
                    "s3": {
                        "object": {
                            "key": self.s3objectkey,
                        },
                        "bucket": {
                            "name": self.bucket,
                        },
                    },
                }
            ]
        }

    @mock_s3
    @mock_dynamodb2
    def test_extractMetadata(self):
        dynamodb = set_up_dynamodb_client(table=self.table)
        s3 = set_up_s3(
                 bucket=self.bucket,
                 s3objectkey=self.s3objectkey,
                 file_name=self.file_name
             )

        extractMetadata(self.event, None)

        item = dynamodb.get_item(
            TableName=self.table,
            Key={'s3objectkey': {'S': self.s3objectkey}}
        )

        s3objectkey = item['Item']['s3objectkey']['S']
        width = item['Item']['body']['M']['width']['N']
        height = item['Item']['body']['M']['height']['N']
        file_size = item['Item']['body']['M']['file_size']['N']

        self.assertEqual(s3objectkey, self.s3objectkey)
        self.assertEqual(width, '50')
        self.assertEqual(height, '50')
        self.assertEqual(file_size, '10033')

    def tearDown(self):
        os.remove(self.file_name)
