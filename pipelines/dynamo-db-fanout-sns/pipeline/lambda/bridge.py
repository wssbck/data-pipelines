import boto3
import json
import os


sns = boto3.client('sns')
sns_arn = os.environ['SNS_TOPIC']


def handler(event, context):

    dynamodb_entry = event['Records'][0]['dynamodb']
    sns_message = json.dumps(dynamodb_entry)

    response = sns.publish(
        TopicArn=sns_arn,
        Message=sns_message,
    )

    return response
