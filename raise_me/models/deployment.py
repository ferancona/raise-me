from dataclasses import dataclass, field
from typing import List

from .event import RaiseEvent


@dataclass
class Deployment:
    events: List[RaiseEvent] = field(default_factory=list)

    def __post__init__(self):
        self.events.sort(key=lambda e: e.logical_name)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Deployment):
            return str(self) == str(__o)
        return False

    def __str__(self) -> str:
        return '{{Events: {}}}'.format([str(e) for e in self.events])