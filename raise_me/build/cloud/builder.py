import pathlib
from typing import Dict, List, Union

from .aws import AWSCloud
from .gcp import GCPCloud
from raise_me.models import Deployment, RaiseEvent
from raise_me.parser import ConfigParser, DeploymentParser


class CloudBuilder:
    def __init__(self, config_path: Union[str, pathlib.Path]) -> None:
        self.conf: Dict = ConfigParser.from_yaml(path=config_path)
    
    def update_stack(self, events_path: Union[str, pathlib.Path]) -> None:
        deployment: Deployment = DeploymentParser.from_yaml(path=events_path)
        
        aws_events: List[RaiseEvent] = [event for event in deployment.events 
                                        if event.source.provider == 'aws']
        gcp_events: List[RaiseEvent] = [event for event in deployment.events 
                                        if event.source.provider == 'gcp']

        if len(aws_events) > 0:
            AWSCloud(config=self.conf).update_stack(events=aws_events)
        
        if len(gcp_events) > 0:
            GCPCloud(config=self.conf).update_stack(events=gcp_events)