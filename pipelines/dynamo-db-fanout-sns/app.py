#!/usr/bin/env python3

from aws_cdk.core import App

from pipeline.pipeline_stack import PipelineStack


app = App()
PipelineStack(app, "dynamo-db-fanout-sns", env={'region': 'eu-central-1'})

app.synth()
