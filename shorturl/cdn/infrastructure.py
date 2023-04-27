import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins
from constructs import Construct


class CDN(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        api_gateway_endpoint: str,
    ):
        
        super().__init__(scope, id_)
        
        api_gateway_origin = origins.HttpOrigin(api_gateway_endpoint)
	    
        distribution = cloudfront.Distribution(
            self, 
            "Distribution",
            default_behavior=cloudfront.BehaviorOptions(origin=api_gateway_origin),
        )