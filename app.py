#!/usr/bin/env python3
import os

import aws_cdk as cdk

import constants
from shorturl.component import ShortURL


app = cdk.App()

backend = ShortURL(
    app,
    constants.APP_NAME + "Sandbox",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
)

app.synth()
