import unittest
import boto3
from moto import mock_s3, mock_dynamodb2
from handler import extractMetadata
from PIL import Image
import os


class TestHandlerFunctions(unittest.TestCase):

    def setUp(self):
        self.bucket = 'teste'
        self.s3objectkey = 'image-001'
        self.table = 'images'
        self.file_name = 'image.png'

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

    def set_up_dynamodb(self):
        dynamodb = boto3.client('dynamodb', region_name='us-east-1')
        dynamodb.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 's3objectkey',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 's3objectkey',
                    'KeyType': 'HASH'
                },
            ],
            TableName=self.table,
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        return dynamodb

    def set_up_s3(self):
        image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
        image.save(self.file_name, 'PNG')

        s3_conn = boto3.resource('s3', region_name='us-east-1')
        s3_conn.create_bucket(Bucket=self.bucket)
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.upload_file(
            Bucket=self.bucket,
            Key=self.s3objectkey,
            Filename=self.file_name
        )

        return s3

    @mock_s3
    @mock_dynamodb2
    def test_extractMetadata(self):
        dynamodb = self.set_up_dynamodb()
        s3 = self.set_up_s3()

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
