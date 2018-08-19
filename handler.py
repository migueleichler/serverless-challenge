# coding=utf-8
import boto3


def extractMetadata(event, context):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table('images')

    record = event['Records'][0]
    s3objectkey = record['s3']['object']['key']

    table.put_item(
        Item={
            's3objectkey': s3objectkey,
            'body': 'teste'
        }
    )


def getMetadata(event, context):
    print("Hello World")
