from typing import List

from raise_me import PROVIDERS
from raise_me.models import EventSource


class EventSourceParser:
    VALID_KEYS = (
        'provider', 
        'filters',
    )

    @classmethod
    def from_dict(cls, source: dict) -> EventSource:
        return EventSource(
            provider=source['provider'],
            filters=source['filters'],
        )

    @classmethod
    def valid(cls, source: dict) -> bool:
        """Validates source syntax in terms of key values and types."""
        valid_keys = 'provider' in source and \
            all((key in cls.VALID_KEYS for key in source.keys()))

        if not valid_keys:
            return False
        
        if not isinstance(source['provider'], str) or \
                source['provider'] not in PROVIDERS:
            return False
        
        # Validate 'filters' is a non-empty List[str].
        if 'filters' in source.keys() and (
                not isinstance(source['filters'], List) or 
                len(source['filters']) == 0 or
                not all([isinstance(f, str) for f in source['filters']])):
            return False
        
        return True