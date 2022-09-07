from enum import Enum

from .raise_event import RaiseEvent
from .source import EventSource
from .target import EventTarget, HttpTarget, CustomTarget


class HttpMethod(Enum):
    GET='get'