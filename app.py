#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import RemovalPolicy

import constants
from shorturl.component import ShortURL
from toolchain.component import Toolchain


app = cdk.App()

HOSTED_ZONE_ID = "Z07660041MXSMFM5F1KCM"
ZONE_NAME = "staging.shortr.org"

staging = ShortURL(
    app,
    constants.APP_NAME + "Staging",
    env=cdk.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
    api_lambda_reserved_concurrency=1,
    zone_name=ZONE_NAME,
    hosted_zone_id=HOSTED_ZONE_ID,
    removal_policy=RemovalPolicy.DESTROY,
)

toolchain = Toolchain(
    app,
    constants.APP_NAME + "Toolchain",
    env=cdk.Environment(
        account="642365414278",
        region="us-east-1",
    ),
)

app.synth()
