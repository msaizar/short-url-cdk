import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_backup as backup

from constructs import Construct


class Database(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        *,
        removal_policy: str,
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
            removal_policy=removal_policy,
        )

        vault = backup.BackupVault(
            self,
            "Vault",
            removal_policy=removal_policy,
        )

        plan = backup.BackupPlan.daily35_day_retention(self, "Plan", backup_vault=vault)

        plan.add_selection(
            "Selection",
            resources=[
                backup.BackupResource.from_dynamo_db_table(self.dynamodb_table),
            ],
        )
