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


client = boto3.client('apigatewaymanagementapi', endpoint_url="https://nj87v6wtpf.execute-api.us-east-1.amazonaws.com/production")

def sendMessage(message):
    dynamodb = boto3.resource('dynamodb')
    connectedUsersTable = dynamodb.Table('TA_ConnectedUsers')

    response = connectedUsersTable.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = connectedUsersTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    dynamodb = None
    connectedUsersTable = None

    for connection in data:
        connectionId = connection['connectionId']
        print("Connection id: {}".format(connectionId))
        try:
            response = client.post_to_connection(ConnectionId=connectionId, Data=message)
            print(response)
        except Exception as e:
            print(e)

            if dynamodb == None or connectedUsersTable == None:
                dynamodb = boto3.resource('dynamodb')
                connectedUsersTable = dynamodb.Table('TA_ConnectedUsers')

            print("Removing connection: {}".format(connectionId))
            connectedUsersTable.delete_item(
                Key={
                    'connectionId': connectionId,
                }
            )

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

    start = 0
    take = 50

    queryTags = []
    if "tags" in queryStringParameters:
        queryTags = queryStringParameters["tags"].split(',')
        queryTags = [tag for tag in queryTags if tag != '']

    if "start" in queryStringParameters:
        start = int(queryStringParameters["start"])

    if "take" in queryStringParameters:
        take = int(queryStringParameters["take"])

    sort = "created-desc"
    if "sort" in queryStringParameters:
        sort = queryStringParameters["sort"]

    notebookId = queryStringParameters['notebookId']
    dynamodb = boto3.resource('dynamodb')
    snippetsTable = dynamodb.Table('TA_Snippets')

    response = snippetsTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId))
    items = response['Items']

    while 'LastEvaluatedKey' in response:
        response = snippetsTable.query(KeyConditionExpression=Key('notebookId').eq(notebookId), ExclusiveStartKey=response['LastEvaluatedKey'])

        items.extend(response['Items'])

    print("Item count: {}, query tags: {}".format(len(items), queryTags))

    if len(queryTags) > 0:
        filtered_items = []
        for item in items:
            item_tags = item['tags'].split(',')
            tag_match = False
            for tag in queryTags:
                if tag in item_tags:
                    tag_match = True
                    break
            if tag_match:
                filtered_items.append(item)

        items = filtered_items
    else:
        items = [item for item in items if not "trash" in item['tags'].split(',')]

    print("Item count: {}".format(len(items)))

    if sort == "created-desc":
        snippets = sorted(items, key=lambda a: a['created'], reverse=True)
    elif sort == "created-asc":
        snippets = sorted(items, key=lambda a: a['created'], reverse=False)
    elif sort == "edited-desc":
        snippets = sorted(items, key=lambda a: a['updated'], reverse=True)
    elif sort == "edited-asc":
        snippets = sorted(items, key=lambda a: a['updated'], reverse=False)
    else:
        print("WARNING: UNRECOGNIZED SORT OPTION: {}".format(sort))
        snippets = sorted(items, key=lambda a: a['created'], reverse=True)

    snippets = snippets[start:start + take]

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
    
    isStarred = False
    if 'isStarred' in body:
        isStarred = body['isStarred']

    print("IS STARRED VALUE: {}".format(isStarred))
    print("body: {}".format(body))

    update_result = table.update_item(
        Key={
            'notebookId': notebookId,
            'userId-snippetId': '{}-{}'.format(userId, snippetId)},
        UpdateExpression="set body = :b, title = :tt, tags = :tg, updated = :up, isStarred = :st",
         ExpressionAttributeValues={
        ':b': body['body'],
        ':tt': body['title'],
        ':tg': body['tags'],
        ':up': getTimeStr(),
        ':st': isStarred,
    })

    to_write = {
        'notebookId': notebookId,
        'userId-snippetId': '{}-{}'.format(userId, snippetId),
        'userId': userId,
        'snippetId': snippetId,
        'updated': getTimeStr(),
        'title': body['title'],
        'body': body['body'],
        'tags': body['tags'],
        'isStarred': isStarred,
    }

    sendMessage(json.dumps(to_write))

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
        'isStarred': False,
        'title': body['title'],
        'body': body['body'],
        'tags': body['tags'],
    }

    to_write = json.loads(json.dumps(to_write), parse_float=Decimal)

    result = table.put_item(
        Item=to_write
    )

    sendMessage(json.dumps(to_write))
    
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


def connectionHandler(event, context):
    print(event)
    print(context)
        
    connectionId = event["requestContext"]["connectionId"]
    dynamodb = boto3.resource('dynamodb')
    connectedUsersTable = dynamodb.Table('TA_ConnectedUsers')

    to_write = {
        'connectionId': connectionId,
        'created': getTimeStr()
    }
    
    to_write = json.loads(json.dumps(to_write), parse_float=Decimal)

    print("to write: {}".format(to_write))

    result = connectedUsersTable.put_item(
        Item=to_write
    )


    return {"statusCode": 200}

def defaultHandler(event, context):
    print(event)
    print(context)
    connectionId = event["requestContext"]["connectionId"]
    dynamodb = boto3.resource('dynamodb')
    connectedUsersTable = dynamodb.Table('TA_ConnectedUsers')

    connectedUsersTable.delete_item(
        Key={
            'connectionId': connectionId,
        }
    )
    
    return {"statusCode": 200}

def sendMessageHandler(event, context):
    print(event)
    body = json.loads(event['body'])
    message = body['message']
    print("message")
    print(message)

    # check the password
    # if the password is there, blast out the message to everyone
    sendMessage(message)    

    return { "statusCode": 200  }

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
