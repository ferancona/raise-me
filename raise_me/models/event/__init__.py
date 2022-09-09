from enum import Enum

from raise_me.exceptions import UnrecognizedHttpMethod

from .raise_event import RaiseEvent
from .source import EventSource
from .target import EventTarget, HttpTarget, CustomTarget


class HttpMethod(Enum):
    GET='get'

    @classmethod
    def from_str(cls, val: str) -> "HttpMethod":
        if val == 'get': 
            return HttpMethod.GET
        raise UnrecognizedHttpMethod(val)