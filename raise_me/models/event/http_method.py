from enum import Enum

from raise_me.exceptions import UnrecognizedHttpMethod


class HttpMethod(Enum):
    GET='get'
    POST='post'

    @classmethod
    def from_str(cls, val: str) -> "HttpMethod":
        if val == 'get': 
            return HttpMethod.GET
        elif val == 'post': 
            return HttpMethod.POST
        raise UnrecognizedHttpMethod(val)