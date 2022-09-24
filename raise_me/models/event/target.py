from abc import ABC, abstractmethod
from dataclasses import dataclass

from .http_method import HttpMethod


class EventTarget(ABC):
    @abstractmethod
    def json(self):
        raise NotImplementedError()


@dataclass(frozen=True)
class HttpTarget(EventTarget):
    method: HttpMethod
    url: str
    # body: Optional[dict]

    def __str__(self) -> str:
        return f'HttpTarget: {self.method}|{self.url}'

    def json(self):
        return {
            'method': self.method.value,
            'url': self.url,
        }


@dataclass(frozen=True)
class ActionTarget(EventTarget):
    name: str

    def __str__(self) -> str:
        return f'CustomTarget: {self.name}'
    
    def json(self):
        return {
            'name': self.name,
        }