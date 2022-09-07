import pathlib

from dataclasses import dataclass, field
from typing import Dict, List, Union

from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

from raise_me import PROVIDER_SERVICES
from .event import EventSource, EventTarget, RaiseEvent


@dataclass
class Deployment:
    events: List[RaiseEvent] = field(default_factory=list)

    def __post__init__(self):
        self.events.sort(key=lambda e: e.logical_name)

    @classmethod
    def from_yaml(cls, path: Union[str, pathlib.Path]) -> "Deployment":
        p = pathlib.Path(path).resolve()
        try:
            return DeploymentParser.parse_from_yaml(p)
        except SyntaxError as err:
            # Log.
            raise err

    def to_tf_json(self) -> Dict:
        # ? Do I need this here.
        # Actually, I don't think so. This might be the builders work.
        #   More specifically, each provider's builder (e.g., AWSBuilder).

        # Perhaps we could implement this in 
        #   DeploymentBuilder.to_tf_json(
        #       model=deployment, 
        #       provider='aws') 
        #   
        ...

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Deployment):
            return str(self) == str(__o)
        return False

    def __str__(self) -> str:
        return '{{Events: {}}}'.format([str(e) for e in self.events])
    ...


class DeploymentParser:
    @classmethod
    def parse_from_yaml(cls, path: pathlib.Path) -> "Deployment":
        parser = YAML(typ='safe')
        try:
            with open(path, 'r') as f:
                yaml_ = parser.load(f.read())
        except DuplicateKeyError as err:
            # Log. No duplicate keys allowed.
            raise err
        return Deployment(events=cls.parse_events(yaml_=yaml_))
    
    @classmethod
    def parse_events(cls, yaml_: YAML) -> List[RaiseEvent]:
        if 'Events' not in yaml_:
            raise SyntaxError('"Events" configuration not found.')
        
        if not isinstance(yaml_['Events'], dict):
            raise SyntaxError('"Events" configuration not found.')

        raise_events: List[RaiseEvent] = []
        for name, event_meta in yaml_['Events'].items():
            if not cls.valid_source(event_meta['Source']):
                raise SyntaxError('Source from event "{}" malformed: {}.'
                    .format(name, event_meta['Source']))
            for endpoint in event_meta['Targets']:
                if not cls.valid_target(endpoint):
                    raise SyntaxError('Target from event "{}" unreachable: {}.'
                        .format(name, endpoint))
            
            src = event_meta['Source'].split('::')
            raise_events.append(
                RaiseEvent(
                    logical_name=name,
                    source=EventSource(
                        provider=src[0],
                        service=src[1],
                    ),
                    targets=[EventTarget(endpoint=ep) 
                             for ep in event_meta['Targets']])
            )
        return raise_events
    
    @classmethod
    def valid_source(self, src: str) -> bool:
        """Validates RaiseEvent.Source format (e.g., AWS::S3)."""
        split = src.split('::')
        return len(split) == 2 and \
            split[0] in PROVIDER_SERVICES and \
            split[1] in PROVIDER_SERVICES[split[0]]

    @classmethod
    def valid_target(self, endpoints: List[str]) -> bool:
        # TODO: Check if endpoints are reachable.
        ...
        return True