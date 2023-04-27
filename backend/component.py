from backend.api.infrastructure import API
from backend.database.infrastructure import Database

from typing import Any

import aws_cdk as cdk
from constructs import Construct


class Backend(cdk.Stack):
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