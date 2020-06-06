import json
import pytest

from aws_cdk import core
from dynamo-db-streaming.dynamo_db_streaming_stack import DynamoDbStreamingStack


def get_template():
    app = core.App()
    DynamoDbStreamingStack(app, "dynamo-db-streaming")
    return json.dumps(app.synth().get_stack("dynamo-db-streaming").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
