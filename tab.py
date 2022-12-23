import boto3,os
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
load_dotenv()

print('dynamodb connected!!....')

# dynamo_client = boto3.resource( service_name = 'dynamodb',region_name = 'us-east-1',aws_access_key_id = 'AKIA3YAIMTT5G5HFETXH', aws_secret_access_key = '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')
# table = dynamo_client.Table('game_participent')

dynamodb = boto3.resource( service_name = os.getenv('service_name'),region_name = os.getenv('region_name'),aws_access_key_id = os.getenv('aws_access_key_id'), aws_secret_access_key = os.getenv('aws_secret_access_key'))
existing_tables = [table.name for table in dynamodb.tables.all()]
# print(existing_tables)

def run():
    if 'JumbledWord_Engagement' not in existing_tables:  
        dynamodb.create_table(
            TableName='JumbledWord_Engagement',
            KeySchema=[
                {
                    'AttributeName': 'JumbledWord_InitiatedByUser_ID',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'JumbledWord_InitiatedByUser_ID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
        print('create table JumbledWord_Engagement')
    
    if "game_participent" not in existing_tables:
        dynamodb.create_table(
            TableName='game_participent',
            KeySchema=[
                {
                    'AttributeName': 'User_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'User_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
        print('create table game_participent')
     
    if "User_Master" not in existing_tables:
        dynamodb.create_table(
            TableName='User_Master',
            KeySchema=[
                {
                    'AttributeName': 'User_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'User_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
        print('create table User_Master')
    
    if "User_Points" not in existing_tables:
        dynamodb.create_table(
            TableName='User_Points',
            KeySchema=[
                {
                    'AttributeName': 'User_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'User_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
        print('create table User_Points')
     
    if "Telegram_Master" not in existing_tables:
        dynamodb.create_table(
            TableName='Telegram_Master',
            KeySchema=[
                {
                    'AttributeName': 'User_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'User_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        ) 
        print("Table status: Telegram_Master")
    
    if "Quiz_Engagement" not in existing_tables:
        dynamodb.create_table(
            TableName='Quiz_Engagement',
            KeySchema=[
                {
                    'AttributeName': 'User_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'User_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10  
            }
        )
        print('create table Quiz_Engagement')
    
    if "Temp_JumbledWord_Session" not in existing_tables:
        dynamodb.create_table(
            TableName='Temp_JumbledWord_Session',
            KeySchema=[
                {
                    'AttributeName': 'Id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Id',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10  
                }
            )

run()
# db = dynamodb.Table('wowowowoow')
# item = {
#         'artist':'artist',
#         'song':'song',
#         'User_id':'123',
#         'priceUsdCents':'priceUsdCents',
#         'publisher':'publisher'
#         }

# db.put_item( 
#             Item=item
#         )
# print("UPLOADING ITEM")q

# db = dynamodb.Table('Temp_JumbledWord_Session')
# response = db.query()
# data = response['Items']
# print(data)