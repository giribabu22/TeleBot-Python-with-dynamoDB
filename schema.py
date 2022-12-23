import boto3, os
from dotenv import load_dotenv

load_dotenv()

GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
class DynamoDB_con():
    def __init__(self):
        self.dynamo_client = boto3.resource( service_name = os.getenv('service_name'),region_name = os.getenv('region_name'),aws_access_key_id = os.getenv('aws_access_key_id'), aws_secret_access_key = os.getenv('aws_secret_access_key'))

    def  sending(self,data,tableName):
        db = self.dynamo_client.Table(tableName)
        
        db.put_item(
            Item=data
        )
        print('Data is sending!!!!')

    
    def reading(self,tableName):
        table = self.dynamo_client.Table(tableName)
        response = table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        print(data)
        return data,len(data)
    
    
