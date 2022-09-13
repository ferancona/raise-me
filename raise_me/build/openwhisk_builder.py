import pathlib
from typing import List, Union

from requests.models import Response

from raise_me.models import Deployment, HttpTarget, ActionTarget
from raise_me.wsk import WskClient
from raise_me.wsk import HTTP_MEDIATOR_PATH, HTTP_INVOKER_PATH, \
    HTTP_INVOKER_ACTION_NAME


class OpenwhiskBuilder:
    def __init__(self, wsk_client: WskClient) -> None:
        self.wsk_client = wsk_client

    def create_resources(self, deployment: Deployment) -> None:
        """Create Openwhisk Actions, Triggers and Rules that represent the core
        of the event broker system. 

        External provider events will fire specific Triggers that will invoke 
        the corresponding Actions associated to that event to reach all targets
        declared in 'raise-events.yaml'.

        Logic description:
        - Deploy 'raise-http-invoker' action, receives (event, http_target).
        - Create event trigger (can be fired externally).
        - For each action_target:
            - Create rule to link trigger to action_target.
        - If at least 1 http_target, create http_mediator, which will invoke 
            the 'raise-http-invoker' action for every http_target.
            - For each http_target:
                - Create rule to link trigger to http_mediator.
        """
        # ? Implement logic to handle asynchronous creation of resources?
        
        # Create 'raise-http-invoker' Action.
        _ = self.create_http_invoker(
            name=HTTP_INVOKER_ACTION_NAME,
            wsk_client=self.wsk_client, 
            path=HTTP_INVOKER_PATH,
        )
        
        for event in deployment.events:
            targets_to_mediate: List[HttpTarget] = []
            targets_to_trigger: List[ActionTarget] = []

            for target in event.targets:
                if isinstance(target, HttpTarget):
                    targets_to_mediate.append(target)
                elif isinstance(target, ActionTarget):
                    targets_to_trigger.append(target)
            
            # Create a event trigger.
            trigger_name = f'raise_trigger-{event.logical_name}'
            _ = self.wsk_client.create_trigger(name=trigger_name)

            # Create a rule for every user-defined action_target.
            for target in targets_to_trigger:
                _ = self.wsk_client.create_rule(
                    name=f'raise_rule-{trigger_name}-{target.name}',
                    trigger_name=trigger_name,
                    action_name=target.name,
                )
            
            if len(targets_to_mediate) > 0:
                # Create http-mediator event action and link to trigger.
                event_mediator_name = f'raise_mediator-{event.logical_name}'
                _ = self.create_http_mediator(
                    name=event_mediator_name,
                    http_targets=targets_to_mediate,
                    wsk_client=self.wsk_client,
                    path=HTTP_MEDIATOR_PATH,
                )
                _ = self.wsk_client.create_rule(
                    name=f'raise_rule-{trigger_name}-{event_mediator_name}',
                    trigger_name=trigger_name,
                    action_name=event_mediator_name,
                )

    @classmethod
    def create_http_invoker(cls,
                            name: str,
                            wsk_client: WskClient,
                            path: Union[str, pathlib.Path]) -> Response:
        return wsk_client.create_action(
            name=name,
            runtime='python:3',
            code=open(path, 'r').read(),
            main='main',
        )
    
    @classmethod
    def create_http_mediator(cls,
                             name: str,
                             http_targets: List[HttpTarget],
                             wsk_client: WskClient,
                             path: Union[str, pathlib.Path]) -> Response:
        adapted_code = 'HTTP_TARGETS={}\nAUTH={}\n{}'.format(
            [target.json() for target in http_targets],
            wsk_client.auth,
            open(path, 'r').read(),
        )
        return wsk_client.create_action(
            name=name,
            runtime='python:3',
            code=adapted_code,
            main='main',
        )