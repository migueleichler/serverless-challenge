import unittest
from moto import mock_s3, mock_dynamodb2
from handler import getMetadata
from tests.set_up import set_up_dynamodb_resource


class TestLambdaGetMetadata(unittest.TestCase):

    def setUp(self):
        self.s3objectkey = 'image-001'
        self.table = 'images'
        self.width = '50'
        self.height = '100'
        self.file_size = '130.00'

        self.event = {
            "pathParameters": {
                "s3objectkey": self.s3objectkey,
            }
        }

    @mock_s3
    @mock_dynamodb2
    def test_getMetadata(self):
        dynamodb = set_up_dynamodb_resource(table=self.table)

        table = dynamodb.Table(self.table)
        table.put_item(
            Item={
                's3objectkey': self.s3objectkey,
                'body': {
                    'width': self.width,
                    'height': self.height,
                    'file_size': self.file_size
                }
            }
        )

        response = getMetadata(self.event, None)

        self.assertEqual(response['statusCode'], '200')
        self.assertEqual(response['body']['width'], self.width)
        self.assertEqual(response['body']['height'], self.height)
