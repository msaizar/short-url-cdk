import json
import boto3
import os

client = boto3.client('dynamodb')

def handler(event, context):
  data = {}
  if event['requestContext']['http']['method'] == 'GET':
    data = client.get_item(
      TableName=os.getenv('DYNAMODB_TABLE_NAME'),
      Key={
          'ShortURL': {
            'S': event['rawPath'][1:]
          }
      }
    )
    if 'Item' in data:
      data = data['Item']['FullURL']['S']
    else:
      data = {}

  response = {
    'statusCode': 200,
    'body': json.dumps(data),
    'headers': {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
  }
  
  return response
 