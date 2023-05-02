from shorturl.api.infrastructure import API
from shorturl.database.infrastructure import Database
from shorturl.cdn.infrastructure import CDN
from shorturl.dns.infrastructure import DNS
from shorturl.frontend.infrastructure import Frontend


from typing import Any

import aws_cdk as cdk
from constructs import Construct

import constants


class ShortURL(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        api_lambda_reserved_concurrency: int,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        database = Database(
            self,
            "Database",
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
        )

        cdn = CDN(
            self,
            "CDN",
            api_gateway_endpoint=api_gateway_endpoint,
            frontend_bucket=frontend.frontend_bucket,
            domain_name=f"short-api.{constants.HOSTED_ZONE_NAME}",
        )

        dns = DNS(
            self,
            "DNS",
            hosted_zone_name=constants.HOSTED_ZONE_NAME,
            distribution=cdn.distribution,
        )
