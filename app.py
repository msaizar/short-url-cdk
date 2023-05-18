#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import RemovalPolicy

import constants
from shorturl.component import ShortURL


app = cdk.App()

mikes_sandbox = ShortURL(
    app,
    constants.APP_NAME + "MikeSandbox",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    hosted_zone_name=f"mike.sandbox.{constants.HOSTED_ZONE_NAME}",
    removal_policy=RemovalPolicy.DESTROY,
)

staging = ShortURL(
    app,
    constants.APP_NAME + "Staging",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    hosted_zone_name=f"staging.{constants.HOSTED_ZONE_NAME}",
    removal_policy=RemovalPolicy.DESTROY,
)

production = ShortURL(
    app,
    constants.APP_NAME + "Production",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    hosted_zone_name=constants.HOSTED_ZONE_NAME,
    removal_policy=RemovalPolicy.RETAIN,
)


app.synth()
