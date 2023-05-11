import aws_cdk.aws_route53 as route53
import aws_cdk.aws_route53_targets as route53_targets

from aws_cdk.aws_cloudfront import IDistribution
from constructs import Construct

import constants


class DNS(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        distribution: IDistribution,
    ):
        super().__init__(scope, id_)

        hosted_zone = route53.HostedZone.from_lookup(
            self, "MyZone", domain_name=constants.HOSTED_ZONE_NAME
        )

        route53.ARecord(
            self,
            "Alias",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(distribution)
            ),
            record_name=f"{constants.SUBDOMAIN}.{constants.HOSTED_ZONE_NAME}",
        )
