from backend.api.infrastructure import API

from typing import Any

import aws_cdk as cdk
from constructs import Construct


class Backend(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        api_dynamodb_table_name: str,
        api_lambda_reserved_concurrency: int,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        api = API(
            self,
            "API",
            dynamodb_table_name=api_dynamodb_table_name,
            lambda_reserved_concurrency=api_lambda_reserved_concurrency,
        )