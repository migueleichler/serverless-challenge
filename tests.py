import unittest
import boto3
from moto import mock_s3, mock_dynamodb2
from handler import extractMetadata


class TestHandlerFunctions(unittest.TestCase):

    def setUp(self):
        self.bucket = 'teste'
        self.s3objectkey = 'image-001.jpeg'
        self.table = 'images'

        self.event = {
            "Records": [
                {
                    "s3": {
                        "object": {
                            "key": self.s3objectkey,
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
                {
                    'AttributeName': 'width',
                    'AttributeType': 'N',
                },
                {
                    'AttributeName': 'height',
                    'AttributeType': 'N',
                }
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

    @mock_dynamodb2
    def test_extractMetadata(self):
        dynamodb = self.set_up_dynamodb()

        extractMetadata(self.event, None)

        item = dynamodb.get_item(
            TableName=self.table,
            Key={'s3objectkey': {'S': self.s3objectkey}}
        )

        self.assertEqual(item['Item']['s3objectkey']['S'], self.s3objectkey)
