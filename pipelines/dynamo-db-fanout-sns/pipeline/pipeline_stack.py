import aws_cdk.core as core
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_lambda as lmbd
import aws_cdk.aws_lambda_event_sources as lmbd_src
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as sns_subs
import aws_cdk.aws_sqs as sqs

from os.path import dirname, join as join_path, realpath


queues = ['fanout_queue_1',
          'fanout_queue_2',
          'fanout_queue_3']


class PipelineStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB table
        dynamo_part_key = dynamodb.Attribute(name='order_id',
                                             type=dynamodb.AttributeType.STRING)

        dynamo_table = dynamodb.Table(self, 'dynamo_db_table',
                                      table_name='fanout_dynamo_db_table',
                                      partition_key=dynamo_part_key,
                                      billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                                      stream=dynamodb.StreamViewType.NEW_IMAGE)

        # Lambda function bridging DynamoDB and SNS
        lambda_code_path = join_path(dirname(realpath(__file__)), 'lambda')
        lambda_code = lmbd.Code.from_asset(lambda_code_path)

        lambda_bridge = lmbd.Function(self, 'lambda_bridge',
                                      function_name='lambda_bridge',
                                      code=lambda_code,
                                      handler='bridge.handler',
                                      runtime=lmbd.Runtime.PYTHON_3_7,
                                      environment={},
                                      memory_size=128)

        lambda_evnt_src = lmbd_src.DynamoEventSource(dynamo_table,
                                                starting_position=lmbd.StartingPosition.LATEST,
                                                batch_size=1,
                                                parallelization_factor=1)
        lambda_bridge.add_event_source(lambda_evnt_src)
                     

        # SNS Topic
        sns_topic = sns.Topic(self, 'sns_topic', display_name='sns_topic')
        
        # SQS queues receiving messages from the SNS Topic
        for q in queues:
            sqs_queue = sqs.Queue(self, q, queue_name=q)
            sns_sub = sns_subs.SqsSubscription(sqs_queue)
            sns_topic.add_subscription(sns_sub)

        # Connect Lambda and SNS
        sns_topic.grant_publish(lambda_bridge)
        lambda_bridge.add_environment('SNS_TOPIC', sns_topic.topic_arn)
