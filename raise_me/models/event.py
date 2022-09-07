from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RaiseEvent:
    # id_: str
    logical_name: str
    source: "EventSource"
    targets: List["EventTarget"]

    def __post_init__(self):
        self.targets.sort(key=lambda t: str(t))

    def __eq__(self, __o: object) -> bool:
        return (self.logical_name == __o.logical_name and 
            self.source == __o.source and 
            set([str(t) for t in self.targets]) == 
                set([str(t) for t in __o.targets]))
    
    def __str__(self) -> str:
        return '{{{}: {{Source: \'{}\', Targets: {}}}}}'.format(
            self.logical_name,
            self.source,
            [str(t) for t in self.targets])


@dataclass(frozen=True)
class EventSource:
    provider: str
    service: str

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, EventSource):
            return self.provider == __o.provider and \
                self.service == __o.service
        return False
    
    def __str__(self) -> str:
        return f'{self.provider}::{self.service}'


@dataclass(frozen=True)
class EventTarget:
    endpoint: str

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, EventTarget):
            return self.endpoint == __o.endpoint
        return False
    
    def __str__(self) -> str:
        return f'{self.endpoint}'