from asyncio import constants
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import uuid
import datetime

def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def getNotebook(event, context):
    print("Get notebook")

    print(event)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TA_Snippets')
    notebookId = '124'

    response = table.query(KeyConditionExpression=Key('notebookId').eq(notebookId))
    items = response['Items']
    print(items)

    response = {"statusCode": 200, "body": json.dumps(items)}

    return response
    

def newSnippet(event, context):
    print("NEW SNIPPET")
    print(event)

    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TA_Snippets')

    timestamp = str(datetime.datetime.now())
    notebookId = body['notebookId']
    userId = body['userId']
    snippetId = str(uuid.uuid4()).replace('-', '')
    
    to_write = {
        'notebookId': notebookId,
        'userId-snippetId': '{}-{}'.format(userId, snippetId),
        'timestamp': timestamp,
        'title': body['title'],
        'body': body['body'],
        'tags': body['tags'],
    }

    to_write = json.loads(json.dumps(to_write), parse_float=Decimal)

    result = table.put_item(
        Item=to_write
    )

    response = {"statusCode": 200, "body": json.dumps(result)}

    return response


if __name__ == "__main__":
    newSnippet({}, {})

# handlers for posting a new snippet
# listing snippets - by project
# editing a snippet


# user authentication
#