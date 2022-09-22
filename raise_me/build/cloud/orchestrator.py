import pathlib
from typing import Dict, Union

from . import AWSCloud, GCPCloud
from raise_me.models import Deployment
from raise_me.parser import ConfigParser, DeploymentParser


class CloudOrchestrator:
    def __init__(self, config_path: Union[str, pathlib.Path]) -> None:
        self.conf: Dict = ConfigParser.from_yaml(path=config_path)
        self.aws_cloud = AWSCloud(config=self.conf)
        self.gcp_cloud = GCPCloud(config=self.conf)
    
    def update_stack(self, events_path: Union[str, pathlib.Path]) -> None:
        deployment: Deployment = DeploymentParser.from_yaml(path=events_path)
        
        self.aws_cloud.update_stack(
            events=[event for event in deployment.events 
            if event.source.provider == 'aws'])
        
        self.gcp_cloud.update_stack(
            events=[event for event in deployment.events 
            if event.source.provider == 'gcp'])