import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins
import aws_cdk.aws_certificatemanager as certificatemanager

from constructs import Construct
from aws_cdk.aws_s3 import IBucket

import constants


class CDN(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        api_gateway_endpoint: str,
        frontend_bucket: IBucket,
        domain_name: str,
    ):
        super().__init__(scope, id_)

        api_gateway_origin = origins.HttpOrigin(api_gateway_endpoint)

        domain_cert = certificatemanager.Certificate.from_certificate_arn(
            self, "domainCert", constants.CERTIFICATE_ARN
        )

        origin_access_identity = cloudfront.OriginAccessIdentity(
            self,
            "OriginAccessIdentity",
        )

        s3_origin = origins.S3Origin(
            bucket=frontend_bucket, origin_access_identity=origin_access_identity
        )

        self.distribution = cloudfront.Distribution(
            self,
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=api_gateway_origin,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
            ),
            domain_names=[domain_name],
            certificate=domain_cert,
            default_root_object="index.html",
        )

        self.distribution.add_behavior(path_pattern="/index.html", origin=s3_origin)
        self.distribution.add_behavior(path_pattern="/static/*", origin=s3_origin)
