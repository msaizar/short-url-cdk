from shorturl.api.infrastructure import API
from shorturl.database.infrastructure import Database
from shorturl.cdn.infrastructure import CDN
from shorturl.dns.infrastructure import DNS
from shorturl.frontend.infrastructure import Frontend

from typing import Any
import pathlib

import aws_cdk as cdk
import aws_cdk.aws_s3_deployment as s3_deployment
from constructs import Construct


class ShortURL(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        api_lambda_reserved_concurrency: int,
        zone_name: str,
        hosted_zone_id: str,
        removal_policy: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        database = Database(
            self,
            "Database",
            removal_policy=removal_policy,
        )

        api = API(
            self,
            "API",
            dynamodb_table_name=database.dynamodb_table.table_name,
            lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )

        database.dynamodb_table.grant_read_write_data(api.lambda_function)

        api_gateway_endpoint = f"{api.api_gateway_http_api.http_api_id}.execute-api.{self.region}.amazonaws.com"

        frontend = Frontend(
            self,
            "Frontend",
            removal_policy=removal_policy,
        )

        cdn = CDN(
            self,
            "CDN",
            api_gateway_endpoint=api_gateway_endpoint,
            frontend_bucket=frontend.frontend_bucket,
            hosted_zone_id=hosted_zone_id,
            zone_name=zone_name,
        )

        s3_deployment.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[
                s3_deployment.Source.asset(
                    str(
                        pathlib.Path(__file__)
                        .parent.joinpath("frontend/assets")
                        .resolve()
                    )
                )
            ],
            destination_bucket=frontend.frontend_bucket,
            distribution=cdn.distribution,
            distribution_paths=["/index.html", "/static/*"],
        )

        DNS(
            self,
            "DNS",
            distribution=cdn.distribution,
            hosted_zone_id=hosted_zone_id,
            zone_name=zone_name,
        )
