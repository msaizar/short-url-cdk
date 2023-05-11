#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import RemovalPolicy

import constants
from shorturl.component import ShortURL


app = cdk.App()

sandbox = ShortURL(
    app,
    constants.APP_NAME + "Sandbox",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    subdomain="short-dev",
    hosted_zone_name=constants.HOSTED_ZONE_NAME,
    certificate_arn=constants.CERTIFICATE_ARN,
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
    subdomain="short",
    hosted_zone_name=constants.HOSTED_ZONE_NAME,
    certificate_arn=constants.CERTIFICATE_ARN,
    removal_policy=RemovalPolicy.RETAIN,
)


app.synth()
