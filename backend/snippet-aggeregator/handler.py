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


def getNotebooks(event, context):
    print("Get Notebooks")

    print(event)

    queryStringParameters = event['queryStringParameters']
    print(queryStringParameters)

    userId = queryStringParameters['userId']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TA_Users')

    response = table.query(KeyConditionExpression=Key('userId').eq(userId))
    items = response['Items']
    print(items)
    item = items[0]

    ids = item['notebookIds'].split(',')

    table = dynamodb.Table('TA_Notebooks')

    to_return = []
    for id in ids:
        response = table.query(KeyConditionExpression=Key('notebookId').eq(id))
        item = response['Items'][0]
        to_return.append({
            'id': id,
            'name': item['name']
        })

    response = {"statusCode": 200, "body": json.dumps(to_return)}

    return response

def getNotebook(event, context):
    print("Get notebook")

    print(event)

    queryStringParameters = event['queryStringParameters']
    print(queryStringParameters)

    notebookId = queryStringParameters['notebookId']
    dynamodb = boto3.resource('dynamodb')
    snippetsTable = dynamodb.Table('TA_Snippets')

    response = snippetsTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId))
    items = response['Items']

    items = sorted(items, key=lambda a: a['created'], reverse=True)

    notebooksTable = dynamodb.Table('TA_Notebooks')
    response = notebooksTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId))
    notebook = response['Items'][0]


    response = {
        "statusCode": 200,
        "body": json.dumps({
            'notebook': notebook,
            'snippets': items,
            })
    }

    return response

def getSnippet(event, context):
    print("Get notebook")

    print(event)

    queryStringParameters = event['queryStringParameters']
    print(queryStringParameters)

    notebookId = queryStringParameters['notebookId']
    snippetId = queryStringParameters['snippetId']
    userId = queryStringParameters['userId']
    userId_snippetId = "{}-{}".format(userId, snippetId)
    dynamodb = boto3.resource('dynamodb')
    snippetsTable = dynamodb.Table('TA_Snippets')

    response = snippetsTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId)
    & Key('userId-snippetId').eq(userId_snippetId)
    )

    item = response['Items'][0]

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
    
def getNotebookInfo(event, context):
    print("Get notebook name")

    print(event)

    queryStringParameters = event['queryStringParameters']
    print(queryStringParameters)

    notebookId = queryStringParameters['notebookId']
    dynamodb = boto3.resource('dynamodb')

    notebooksTable = dynamodb.Table('TA_Notebooks')
    response = notebooksTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId))
    notebook = response['Items'][0]

    response = {
        "statusCode": 200,
        "body": json.dumps(notebook)
    }

    return response

def generateUUID():
    return str(uuid.uuid4()).replace('-', '')

def getTimeStr():
    return str(datetime.datetime.now())

def newNotebook(event, context):
    print("NEW NOTEBOOK")
    print(event)

    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TA_Notebooks')

    timestamp = getTimeStr()
    userId = body['userId']
    name = body['name']
    notebookId = body['notebookId']

    to_write = {
        'notebookId': notebookId,
        'userId': userId,
        'created': timestamp,
        'name': name,
    }
    
    to_write = json.loads(json.dumps(to_write), parse_float=Decimal)

    result = table.put_item(
        Item=to_write
    )

    response = {"statusCode": 200, "body": json.dumps(result)}

    users_table = dynamodb.Table('TA_Users')
    response = users_table.query(KeyConditionExpression=Key('userId').eq(userId))
    matchedUser = response['Items'][0]
    notebookIds = matchedUser['notebookIds']

    notebookIds += ",{}".format(notebookId)

    users_table.update_item(
        Key={'userId': userId},
        UpdateExpression="set notebookIds = :i",
         ExpressionAttributeValues={
        ':i': notebookIds,
    },
    )

    return response


def updateNotebook(event, context):
    print("Update notebook")
    print(event)
    body = json.loads(event['body'])

    notebookId = body['notebookId']
    name = body['name']

    dynamodb = boto3.resource('dynamodb')
    notebooksTable = dynamodb.Table('TA_Notebooks')
    result = notebooksTable.update_item(
        Key={'notebookId': notebookId},
        UpdateExpression="set #n = :i",
         ExpressionAttributeValues={
            ':i': name,
        },
        ExpressionAttributeNames={
             "#n": "name"
        })

    response = {"statusCode": 200, "body": json.dumps(result)}
    return response


def newSnippet(event, context):
    print("NEW SNIPPET")
    print(event)

    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TA_Snippets')

    timestamp = getTimeStr()
    notebookId = body['notebookId']
    userId = body['userId']
    snippetId = body['snippetId']
    
    to_write = {
        'notebookId': notebookId,
        'userId-snippetId': '{}-{}'.format(userId, snippetId),
        'userId': userId,
        'snippetId': snippetId,
        'created': timestamp,
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


def deleteSnippet(event, context):
    print("Delete snippet")
    print(event)

    queryStringParameters = event['queryStringParameters']
    print(queryStringParameters)

    notebookId = queryStringParameters['notebookId']
    snippetId = queryStringParameters['snippetId']
    userId = queryStringParameters['userId']
    userId_snippetId = "{}-{}".format(userId, snippetId)
    dynamodb = boto3.resource('dynamodb')
    snippetsTable = dynamodb.Table('TA_Snippets')

    response = snippetsTable.delete_item(
        Key={
        'notebookId': notebookId,
        'userId-snippetId': userId_snippetId
        }
    )
    
    response = {"statusCode": 200, "body": json.dumps(response)}

    return response


if __name__ == "__main__":

    notebookId = "5c5dcfe647794baabe7649da394cf5b4"
    snippetId = "0ba76097490e48fdb00806faf22bdf6a"
    userId = "amichai"

    # queryStringParameters = event['queryStringParameters']
    # notebookId = queryStringParameters['notebookId']

    result = deleteSnippet({'queryStringParameters': {'notebookId': notebookId, 'snippetId': snippetId, 'userId': userId}}, {})
    print(result)


# user authentication
#