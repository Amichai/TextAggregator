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
    if len(items) < 1:
        return {"statusCode": 200, "body": json.dumps([])}

    item = items[0]

    ids = item['notebookIds'].split(',')

    table = dynamodb.Table('TA_Notebooks')

    to_return = []
    for id in ids:
        if id == '':
            continue

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

    snippets = sorted(items, key=lambda a: a['created'], reverse=True)

    notebooksTable = dynamodb.Table('TA_Notebooks')
    response = notebooksTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId))

    items = response['Items']

    if len(items) < 1:
        return {"statusCode": 200, "body": {"message": "notebook not found"}}

    notebook = items[0]

    response = {
        "statusCode": 200,
        "body": json.dumps({
            'notebook': notebook,
            'snippets': snippets,
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

    items = response['Items']

    if len(items) < 1:
        return {"statusCode": 200, "body": {"message": "snippet not found"}}

    item = items[0]

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

    items = response['Items']

    if len(items) < 1:
        return {"statusCode": 200, "body": "notebook not found"}

    notebook = items[0]

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

    print("to write: {}".format(to_write))

    result = table.put_item(
        Item=to_write
    )

    print("wrote notebook")

    response = {"statusCode": 200, "body": json.dumps(result)}

    users_table = dynamodb.Table('TA_Users')
    response = users_table.query(KeyConditionExpression=Key('userId').eq(userId))

    items = response['Items']

    if len(items) < 1:
        print("user not found")
        return {"statusCode": 200, "body": {"message": "user not found"}}

    matchedUser = items[0]
    notebookIds = matchedUser['notebookIds']

    print("notebook ids: {}".format(notebookIds))

    notebookIds += ",{}".format(notebookId)

    update_result = users_table.update_item(
        Key={'userId': userId},
        UpdateExpression="set notebookIds = :i",
         ExpressionAttributeValues={
        ':i': notebookIds,
    },
    )

    print("update item result: {}".format(update_result))


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


def updateSnippet(event, context):
    print("UPDATE SNIPPET")
    print(event)

    body = json.loads(event['body'])

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TA_Snippets')

    notebookId = body['notebookId']
    userId = body['userId']
    snippetId = body['snippetId']
    

    update_result = table.update_item(
        Key={
            'notebookId': notebookId,
            'userId-snippetId': '{}-{}'.format(userId, snippetId)},
        UpdateExpression="set body = :b, title = :tt, tags = :tg, updated = :up",
         ExpressionAttributeValues={
        ':b': body['body'],
        ':tt': body['title'],
        ':tg': body['tags'],
        ':up': getTimeStr(),
    })


    response = {"statusCode": 200, "body": json.dumps(update_result)}

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
        'updated': timestamp,
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
    notebookId = "1e47125270194237a3bc290e81a3980d"
    snippetId = "3399530578dd40f8ac3db7f8bd45bf1b"
    userId = "google-oauth2|103185913888289723018"

    # queryStringParameters = event['queryStringParameters']
    # notebookId = queryStringParameters['notebookId']

    # result = deleteSnippet({'queryStringParameters': {'notebookId': notebookId, 'snippetId': snippetId, 'userId': userId}}, {})
    # print(result)

    evt = {
        'body': 
        json.dumps({
            'body': 'updated body',
            'title': 'updated title',
            'tags': 't1,t2',
            'notebookId': notebookId,
            'userId': userId,
            'snippetId': snippetId,
        })
    }

    updateSnippet(evt, None)


# user authentication
#