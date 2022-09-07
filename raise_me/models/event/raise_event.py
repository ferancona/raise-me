from dataclasses import dataclass
from typing import List

from .target import EventTarget
from .source import EventSource


@dataclass(frozen=True)
class RaiseEvent:
    logical_name: str
    source: EventSource
    targets: List[EventTarget]

    def __post_init__(self):
        self.targets.sort(key=lambda t: str(t))

    def __eq__(self, __o: object) -> bool:
        return (self.logical_name == __o.logical_name
            and self.source == __o.source 
            and set([str(t) for t in self.targets]) == 
                set([str(t) for t in __o.targets]))
    
    def __str__(self) -> str:
        return '{{{}: {{Source: \'{}\', Targets: {}}}}}'.format(
            self.logical_name,
            self.source,
            [str(t) for t in self.targets])