import aws_cdk.aws_s3 as s3
from aws_cdk import RemovalPolicy
from constructs import Construct


class Frontend(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        **kwargs,
    ):
        super().__init__(scope, id_)

        self.frontend_bucket = s3.Bucket(
            self,
            "FrontendBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )
