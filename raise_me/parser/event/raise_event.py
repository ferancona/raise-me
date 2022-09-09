from typing import List

from raise_me.models import RaiseEvent
from raise_me.exceptions import InvalidEvent

from .source import EventSourceParser
from .target import EventTargetParser


class RaiseEventParser:
    @classmethod
    def from_dict(cls, name: str, meta: dict) -> RaiseEvent:
        return RaiseEvent(
            logical_name=name,
            source=EventSourceParser.from_dict(source=meta['source']),
            targets=[EventTargetParser.from_dict(target=t) 
                     for t in meta['targets']],
        )

    @classmethod
    def parse_events(cls, events: dict) -> List[RaiseEvent]:
        raise_events: List[RaiseEvent] = []

        for name, event_meta in events.items():
            # Validate syntax.
            if not isinstance(event_meta['source'], dict) or \
                    not EventSourceParser.valid(source=event_meta['source']):
                raise InvalidEvent('Source from event "{}" malformed: {}.'
                    .format(name, event_meta['source']))
            
            if not isinstance(event_meta['targets'], List) or \
                    len(event_meta['targets']) == 0:
                raise InvalidEvent('Targets from event "{}" malformed: {}.'
                    .format(name, event_meta['targets']))

            for target in event_meta['targets']:
                if not EventTargetParser.valid(target=target):
                    raise InvalidEvent('Target from event "{}" malformed: {}.'
                        .format(name, target))

            # Instantiate model.
            raise_events.append(cls.from_dict(name=name, meta=event_meta))
        
        return raise_events