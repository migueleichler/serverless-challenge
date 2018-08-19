# coding=utf-8
import boto3
from io import BytesIO
from PIL import Image
import sys


def get_image_metadata(s3_bucket, s3objectkey):
    s3 = boto3.resource('s3', region_name='us-east-1')

    obj = s3.Object(bucket_name=s3_bucket, key=s3objectkey)
    obj_body = obj.get()['Body'].read()

    img = Image.open(BytesIO(obj_body))
    width = img.size[0]
    height = img.size[1]
    file_size = sys.getsizeof(img.tobytes())

    return {'width': width, 'height': height, 'file_size': file_size}


def extractMetadata(event, context):
    record = event['Records'][0]
    s3_bucket = record['s3']['bucket']['name']
    s3objectkey = record['s3']['object']['key']

    metadata = get_image_metadata(s3_bucket, s3objectkey)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('images')
    table.put_item(
        Item={
            's3objectkey': s3objectkey,
            'body': metadata
        }
    )


def getMetadata(event, context):
    print("Hello World")
