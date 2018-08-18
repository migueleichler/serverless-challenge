# coding=utf-8

import boto3

dynamodb = boto3.resource("dynamodb", region_name='us-east-1')

def extractMetadata(event, context):
    print("Hello World")

def getMetadata(event, context):
    print("Hello World")
