import pathlib
from typing import Dict, Union

from raise_me.models import Deployment

from .yaml_parser import YAMLParser
from .event import RaiseEventParser


class DeploymentParser:
    @classmethod
    def from_yaml(cls, path: Union[str, pathlib.Path]) -> Deployment:
        yaml_: Dict = YAMLParser.parse(path=path)
        
        if 'Events' not in yaml_:
            raise SyntaxError('"Events" configuration not found.')

        if not isinstance(yaml_['Events'], dict):
            raise SyntaxError('"Events" configuration not found.')
        
        return Deployment(
            events=RaiseEventParser.parse_events(events=yaml_['Events']))