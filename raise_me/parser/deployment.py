import pathlib
from typing import Dict, Union

from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

from raise_me.models import Deployment

from .event import RaiseEventParser


class DeploymentParser:
    @classmethod
    def from_yaml(cls, path: Union[str, pathlib.Path]) -> Deployment:
        path = pathlib.Path(path).resolve()
        parser = YAML(typ='safe')
        try:
            with open(path, 'r') as f:
                yaml_: Dict = parser.load(f.read())
        except DuplicateKeyError as err:
            # Log.
            raise err
        
        if 'Events' not in yaml_:
            raise SyntaxError('"Events" configuration not found.')
        
        if not isinstance(yaml_['Events'], dict):
            raise SyntaxError('"Events" configuration not found.')
        
        return Deployment(
            events=RaiseEventParser.parse_events(events=yaml_['Events']))