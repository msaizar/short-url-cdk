#!/usr/bin/env python3
import os

import aws_cdk as cdk

import constants
from backend.component import Backend


app = cdk.App()

Backend(
    app,
    constants.APP_NAME + "Sandbox",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    api_dynamodb_table_name='DYNAMODB_TABLE_NAME',
)

app.synth()
