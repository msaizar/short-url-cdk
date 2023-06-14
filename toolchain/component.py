from typing import Any

import aws_cdk as cdk
import aws_cdk.aws_codebuild as codebuild
from aws_cdk import pipelines
from aws_cdk import RemovalPolicy
from constructs import Construct

import constants
from shorturl.component import ShortURL


GITHUB_CONNECTION_ARN = "arn:aws:codestar-connections:us-east-1:642365414278:connection/88c1a1b3-3f2e-4a8d-9aa0-f6d3aaa47f16"
GITHUB_OWNER = "msaizar"
GITHUB_REPO = "short-url-cdk"
GITHUB_TRUNK_BRANCH = "main"
PRODUCTION_ENV_NAME = "Production"
PRODUCTION_ENV_ACCOUNT = "463267452836"
PRODUCTION_ENV_REGION = "us-east-1"
HOSTED_ZONE_ID = "Z09406111GDOY2XRRN5V8"
ZONE_NAME = "shortr.org"


class Toolchain(cdk.Stack):
    def __init__(self, scope: Construct, id_: str, **kwargs: Any):
        super().__init__(scope, id_, **kwargs)

        source = pipelines.CodePipelineSource.connection(
            GITHUB_OWNER + "/" + GITHUB_REPO,
            GITHUB_TRUNK_BRANCH,
            connection_arn=GITHUB_CONNECTION_ARN,
        )
        build_spec = {"phases": {"install": {"runtime-versions": {"python": "3.10"}}}}
        synth = pipelines.CodeBuildStep(
            "Synth",
            input=source,
            partial_build_spec=codebuild.BuildSpec.from_object(build_spec),
            install_commands=["./scripts/install-deps.sh"],
            commands=["npx cdk synth"],
            primary_output_directory="cdk.out",
        )
        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            cross_account_keys=True,
            docker_enabled_for_synth=True,
            publish_assets_in_parallel=False,
            synth=synth,
        )
        Toolchain._add_production_stage(pipeline)

    @staticmethod
    def _add_production_stage(pipeline: pipelines.CodePipeline) -> None:
        production = cdk.Stage(
            pipeline,
            PRODUCTION_ENV_NAME,
            env=cdk.Environment(
                account=PRODUCTION_ENV_ACCOUNT, region=PRODUCTION_ENV_REGION
            ),
        )
        ShortURL(
            production,
            constants.APP_NAME + PRODUCTION_ENV_NAME,
            stack_name=constants.APP_NAME + PRODUCTION_ENV_NAME,
            api_lambda_reserved_concurrency=1,
            zone_name=ZONE_NAME,
            hosted_zone_id=HOSTED_ZONE_ID,
            removal_policy=RemovalPolicy.RETAIN,
        )

        smoke_test_commands = [f"curl ${ZONE_NAME}"]
        smoke_test = pipelines.ShellStep(
            "SmokeTest",
            commands=smoke_test_commands,
        )

        pipeline.add_stage(production, post=[smoke_test])
