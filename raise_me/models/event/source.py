from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EventSource:
    provider: str
    filters: List[str]

    def __post_init__(self):
        self.filters.sort()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, EventSource):
            return self.provider == __o.provider and \
                set(self.filters) == set(__o.filters)
        return False
    
    def __str__(self) -> str:
        return f'EventSource: {self.provider}|{self.filters}'