from abc import ABC
from dataclasses import dataclass

from . import HttpMethod


class EventTarget(ABC):
    pass


@dataclass(frozen=True)
class HttpTarget(EventTarget):
    method: HttpMethod
    url: str
    # body: Optional[dict]

    def __str__(self) -> str:
        return f'HttpTarget: {self.method}|{self.url}'


@dataclass(frozen=True)
class CustomTarget(EventTarget):
    filename: str

    def __str__(self) -> str:
        return f'CustomTarget: {self.filename}'