from typing import List
import pytest

from raise_me.build import OpenwhiskBuilder
from raise_me.models import Deployment, ActionTarget, HttpTarget
from raise_me.identity.openwhisk import OWResourceIdentifier
from raise_me.wsk import WskClient, WskPaginator


@pytest.fixture
def builder(client) -> OpenwhiskBuilder:
    return OpenwhiskBuilder(wsk_client=client)


@pytest.fixture
def action_names(deployment: Deployment) -> List[str]:
    """
    Check for 1 http_invoker and 1 http_mediator for each event that has at 
    least 1 HttpTarget.
    """
    actions: List[str] = []
    actions.append(OWResourceIdentifier.http_invoker())
    for event in deployment.events:
        if any([isinstance(target, HttpTarget) for target in event.targets]):
            actions.append(OWResourceIdentifier.http_mediator(
                event_name=event.logical_name))
    return actions


@pytest.fixture
def trigger_names(deployment: Deployment) -> List[str]:
    """Check for 1 trigger for each event."""
    return [OWResourceIdentifier.trigger(event_name=event.logical_name) 
            for event in deployment.events]


@pytest.fixture
def rule_names(deployment: Deployment) -> List[str]:
    """
    Check for 1 rule for every ActionTarget in an event and 1 rule for 
    every event that has at least 1 HttpTarget.
    """
    rules = []
    for event in deployment.events:
        action_targets = [target.name for target in event.targets 
                          if isinstance(target, ActionTarget)]
        trigger_name = OWResourceIdentifier.trigger(
            event_name=event.logical_name)
        
        rules += [
            OWResourceIdentifier.rule(
                trigger_name=trigger_name,
                target_name=t.name
            )
            for t in action_targets
        ]
        if any([isinstance(target, HttpTarget) for target in event.targets]):
            rules.append(OWResourceIdentifier.rule(
                trigger_name=trigger_name,
                target_name=OWResourceIdentifier.http_mediator(
                    event_name=event.logical_name
                )
            ))
    return rules


@pytest.mark.builder
class TestOpenwhiskBuilder:
    @pytest.fixture
    def action_paginator(self, client: WskClient):
        return WskPaginator(client=client, resource='action')
    
    @pytest.fixture
    def trigger_paginator(self, client: WskClient):
        return WskPaginator(client=client, resource='trigger')
    
    @pytest.fixture
    def rule_paginator(self, client: WskClient):
        return WskPaginator(client=client, resource='rule')
    
    def test_create_list_destroy_resources(self,
                                           builder: OpenwhiskBuilder, 
                                           deployment: Deployment,
                                           action_paginator: WskPaginator,
                                           trigger_paginator: WskPaginator,
                                           rule_paginator: WskPaginator,
                                           action_names: List[str],
                                           trigger_names: List[str],
                                           rule_names: List[str]):
        """Verify raise-me OpenWhisk resources are created and deleted."""
        builder.create_resources(deployment=deployment)

        actions = set(list(action_paginator.paginate()))
        triggers = set(list(trigger_paginator.paginate()))
        rules = set(list(rule_paginator.paginate()))

        assert set(action_names).issubset(actions) and \
            set(trigger_names).issubset(triggers) and \
            set(rule_names).issubset(rules)
        
        builder.destroy_resources()

        actions = set(list(action_paginator.paginate()))
        triggers = set(list(trigger_paginator.paginate()))
        rules = set(list(rule_paginator.paginate()))

        assert set(action_names).isdisjoint(actions) and \
            set(trigger_names).isdisjoint(triggers) and \
            set(rule_names).isdisjoint(rules)


# def test_s3_to_cloudfunction():
#     ...