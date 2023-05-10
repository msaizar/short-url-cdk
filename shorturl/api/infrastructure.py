import pathlib

import aws_cdk.aws_apigatewayv2_alpha as apigatewayv2_alpha
import aws_cdk.aws_apigatewayv2_integrations_alpha as apigatewayv2_integrations_alpha
import aws_cdk.aws_lambda as lambda_

from constructs import Construct


class API(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        dynamodb_table_name: str,
        lambda_reserved_concurrency: int,
    ):
        super().__init__(scope, id_)

        self.lambda_function = lambda_.Function(
            self,
            "LambdaFunction",
            code=lambda_.Code.from_asset(
                str(pathlib.Path(__file__).parent.joinpath("runtime").resolve())
            ),
            runtime=lambda_.Runtime.PYTHON_3_8,
            environment={"DYNAMODB_TABLE_NAME": dynamodb_table_name},
            reserved_concurrent_executions=lambda_reserved_concurrency,
            handler="index.handler",
        )

        api_gateway_http_lambda_integration = (
            apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                "APIGatewayHTTPLambdaIntegration", handler=self.lambda_function
            )
        )

        self.api_gateway_http_api = apigatewayv2_alpha.HttpApi(
            self,
            "APIGatewayHTTPAPI",
            default_integration=api_gateway_http_lambda_integration,
        )
