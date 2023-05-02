import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins
import aws_cdk.aws_certificatemanager  as certificatemanager
from constructs import Construct

import constants


class CDN(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        api_gateway_endpoint: str,
        domain_name: str,
    ):
        
        super().__init__(scope, id_)
        
        api_gateway_origin = origins.HttpOrigin(api_gateway_endpoint)

        domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "domainCert", constants.CERTIFICATE_ARN)

        self.distribution = cloudfront.Distribution(
            self, 
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(origin=api_gateway_origin),
            domain_names=[domain_name],
            certificate=domain_cert,
        )