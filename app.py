#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import RemovalPolicy

import constants
from shorturl.component import ShortURL
from toolchain.component import Toolchain


app = cdk.App()


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

toolchain = Toolchain(
    app,
    constants.APP_NAME + "Toolchain",
    env=cdk.Environment(
        account=os.environ["CICD_ACCOUNT"],
        region="us-east-1",
    ),
)

app.synth()
