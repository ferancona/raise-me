from typing import Dict, List

import pulumi
import pulumi_gcp as gcp

from . import WORKFLOW_TRIGGER_PATH
from raise_me.identity.openwhisk import OWResourceIdentifier
from raise_me.models import RaiseEvent
from raise_me.parser import FilterParser
from raise_me.util import GCPWorkflowAdapter


class GCPCloud:
    def __init__(self, config: Dict) -> None:
        self.conf = config
        self.account_id = config['gcp']['account-id']
        self.project_id = config['gcp']['project-id']
        self.region = config['gcp']['region']
        self.wf_helper = GCPWorkflowAdapter(
            config=config,
            workflow_path=WORKFLOW_TRIGGER_PATH,
        )

    def update_stack(self, events: List[RaiseEvent]):
        """
        
        Creates the following resources:
        - For every event.source:
            - Workflow:
                - Receives event.
                - Makes API call to corresponding openwhisk trigger.
            - Eventrac Trigger: Triggers workflow from event.
        """
        if len(events) > 0:
            for event in events:
                service_account = gcp.serviceaccount.Account(
                    resource_name='raise-me_service-account',
                    account_id='raise-me-service-account',
                    display_name='Raise-Me Service Account',
                )

                workflows_iam_bind = gcp.projects.IAMMember(
                    resource_name='raise-me_iam-bind_workflows-invoker',
                    project=self.project_id,
                    member=service_account.email.apply(
                        lambda email: f'serviceAccount:{email}'),
                    role='roles/workflows.invoker',
                )
                eventrac_iam_bind = gcp.projects.IAMMember(
                    resource_name='raise-me_iam-bind_eventrac-eventReceiver',
                    project=self.project_id,
                    member=service_account.email.apply(
                        lambda email: f'serviceAccount:{email}'),
                    role='roles/eventarc.eventReceiver',
                )

                workflow = gcp.workflows.Workflow(
                    resource_name=f'raise-me_workflow_{event.logical_name}',
                    region=self.region,
                    description=f'Route raise-me event {event.logical_name}' \
                        'to fire OpenWhisk Trigger.',
                    service_account=service_account.id,
                    project=self.project_id,
                    source_contents=self.wf_helper.to_pulumi_str(
                        trigger_name=OWResourceIdentifier.trigger(
                            event_name=event.logical_name,
                        ),
                    ),
                )

                filters: List[Dict[str, str]] = FilterParser \
                    .to_eventrac_filters(filters=event.source.filters)

                trigger = gcp.eventarc.Trigger(
                    resource_name='raise-me-eventrac-trigger-{}'.format(
                        event.logical_name,
                    ),
                    opts=pulumi.ResourceOptions(depends_on=[
                        workflows_iam_bind, eventrac_iam_bind
                    ]),
                    location=self.region,
                    project=self.project_id,
                    matching_criterias=[
                        gcp.eventarc.TriggerMatchingCriteriaArgs(
                            attribute=f['attribute'],
                            value=f['value'],
                        )
                        for f in filters
                    ],
                    destination=gcp.eventarc.TriggerDestinationArgs(
                        workflow=workflow.name,
                    ),
                    service_account=service_account.name,
                )