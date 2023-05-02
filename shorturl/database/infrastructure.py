import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import RemovalPolicy

from constructs import Construct


class Database(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        **kwargs,
    ):
        super().__init__(scope, id_)

        partition_key = dynamodb.Attribute(
            name="ShortURL",
            type=dynamodb.AttributeType.STRING,
        )

        self.dynamodb_table = dynamodb.Table(
            self,
            "Table",
            partition_key=partition_key,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
