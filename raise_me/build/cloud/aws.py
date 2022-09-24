import json
from typing import Dict, List

import pulumi
import pulumi_aws as aws

from . import CLOUDEVENTS_LAYER_PATH, LAMBDA_TRIGGER_PATH
from raise_me.models import RaiseEvent
from raise_me.identity.openwhisk import OWResourceIdentifier
from raise_me.parser import FilterParser


class AWSCloud:
    def __init__(self, config: Dict) -> None:
        self.conf = config
        self.event_bus_name = config['aws']['event-bus-name']

    def update_stack(self, events: List[RaiseEvent]):
        """

        Creates the following resources:
        - EventBridge Event Bus.
        - Lambda layer for 'cloudevents' python module.
        - For each event.source:
            - Lambda:
                - Converts AWS event to CloudEvent format.
                - Fires Openwhisk Trigger via REST API.
            - Event Rule: triggers Lambda from event.
        """
        if len(events) > 0:
            event_bus = aws.cloudwatch.EventBus(
                resource_name=self.event_bus_name,
                name=self.event_bus_name,
            )
            
            cloudevents_layer = aws.lambda_.LayerVersion(
                resource_name='aws_lambda_cloudevents-layer',
                compatible_runtimes=['python3.7', 'python3.8', 'python3.9'],
                code=pulumi.FileArchive(path=str(CLOUDEVENTS_LAYER_PATH)),
                layer_name='raise-me_{}'.format(
                    CLOUDEVENTS_LAYER_PATH.stem.replace('.', '_')),
            )

            lambda_role = aws.iam.Role(
                resource_name='raise-me_iam-role_lambda',
                assume_role_policy=json.dumps({
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Action': 'sts:AssumeRole',
                        'Principal': {
                            'Service': 'lambda.amazonaws.com'
                        },
                        'Effect': 'Allow',
                        'Sid': ''
                    }],
                }),
            )
            
            for event in events:
                ow_conf: Dict = self.conf['openwhisk']

                event_lambda = aws.lambda_.Function(
                    resource_name=f'aws_lambda-function_{event.logical_name}',
                    code=str(LAMBDA_TRIGGER_PATH),
                    role=lambda_role.arn,
                    handler='openwhisk_trigger.handler',
                    runtime='python3.8',
                    environment=aws.lambda_.FunctionEnvironmentArgs(
                        variables={
                            'TRIGGER_NAME': OWResourceIdentifier.trigger(
                                event_name=event.logical_name),
                            'OW_URL': ow_conf['endpoint'],
                            "OW_USER": ow_conf['auth']['username'],
                            'OW_PASS': ow_conf['auth']['password'],
                        },
                    ),
                    layers=[cloudevents_layer.arn],
                )

                event_rule = aws.cloudwatch.EventRule(
                    resource_name=f'aws_event-rule_{event.logical_name}',
                    description='Route raise-me event ' \
                        f'"{event.logical_name}" to lambda function. ' \
                        'Converts event into CloudEvents format and fires ' \
                        'OpenWhisk Trigger.',
                    event_bus_name=event_bus.name,
                    event_pattern=FilterParser.to_aws_event_pattern(
                        filters=event.source.filters),
                    name=event.logical_name,
                    is_enabled=True,
                )

                event_target = aws.cloudwatch.EventTarget(
                    resource_name=f'aws_event-target_{event.logical_name}',
                    rule=event_rule.name,
                    arn=event_lambda.arn,
                )