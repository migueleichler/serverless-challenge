from PIL import Image
import boto3


def set_up_dynamodb_table(dynamodb, table):
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
        TableName=table,
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )


def set_up_dynamodb_client(table):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    set_up_dynamodb_table(dynamodb, table)

    return dynamodb


def set_up_dynamodb_resource(table):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    set_up_dynamodb_table(dynamodb, table)

    return dynamodb


def set_up_s3(bucket, s3objectkey, file_name):
    image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
    image.save(file_name, 'PNG')

    s3_conn = boto3.resource('s3', region_name='us-east-1')
    s3_conn.create_bucket(Bucket=bucket)
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.upload_file(
        Bucket=bucket,
        Key=s3objectkey,
        Filename=file_name
    )

    return s3
