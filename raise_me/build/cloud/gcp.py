from typing import Dict, List

import pulumi_gcp as gcp

from . import WORKFLOW_TRIGGER_PATH
from raise_me.identity import OWResourceIdentifier
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
        if len(events) > 0:
            for event in events:
                service_account = gcp.serviceaccount.Account(
                    resource_name='raise-me_service-account',
                    account_id=self.account_id,
                    display_name='Raise-Me Service Account',
                )

                workflow = gcp.workflows.Workflow(
                    resource_name=f'raise-me_workflow_{event.logical_name}',
                    region=self.region,
                    description='',
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
                    resource_name='raise-me_eventrac-trigger_{}'.format(
                        event.logical_name,
                    ),
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
                )