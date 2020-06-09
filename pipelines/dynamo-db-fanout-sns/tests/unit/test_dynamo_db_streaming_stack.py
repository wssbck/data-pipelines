import json
import pytest

from aws_cdk import core
from pipeline.pipeline_stack import PipelineStack


@pytest.fixture
def cf_template():
    app = core.App()
    PipelineStack(app, "dynamo-db-fanout")
    return json.dumps(app.synth().get_stack("dynamo-db-fanout").template)


def test_sqs_queue_created(cf_template):
    assert("AWS::SQS::Queue" in cf_template)


def test_sns_topic_created(cf_template):
    assert("AWS::SNS::Topic" in cf_template)
