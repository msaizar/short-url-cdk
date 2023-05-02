import pathlib

import aws_cdk.aws_s3_deployment as s3_deployment
import aws_cdk.aws_s3 as s3

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
        )

        s3_deployment.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[
                s3_deployment.Source.asset(
                    str(pathlib.Path(__file__).parent.joinpath("assets").resolve())
                )
            ],
            destination_bucket=self.frontend_bucket,
        )
