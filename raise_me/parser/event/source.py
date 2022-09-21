import json
from typing import Dict, List, Union

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
        if 'filters' in source.keys():
            if not FilterParser.valid(filters=source['filters'], 
                    provider=source['provider']):
                return False
        
        return True


class FilterParser:

    @classmethod
    def to_aws_event_pattern(cls, 
                             filters: List[str],
                            ) -> Dict[str, Union[str, List, Dict]]:
        filters = filters.copy()
        for index, f in enumerate(filters):
            separator_index = f.index(':')
            key, val = f[:separator_index], f[separator_index:]
            filters[index] = (key, val)
        
        return json.dumps({key: val for key, val in filters})
    
    @classmethod
    def to_eventrac_filters(cls, filters: List[str]) -> List[str]:
        return filters

    @classmethod
    def valid(cls, filters: List[str], provider: str) -> bool:
        """Validates filters syntax in terms of accepted provider formats.
        
        AWS event patterns are composed by key/value pairs separated by ':'.
        GCP Eventrac filters are composed by key/value pairs separated by '='.
        """

        if not isinstance(filters, List) or \
                len(filters) == 0 or \
                not all([isinstance(f, str) for f in filters]):
            return False
        
        split_char = ':' if provider == 'aws' else '='
        for f in filters:
            split = f.split(split_char)
            if len(split) < 2 or (len(split[0]) == 0 or len(split[1]) == 0):
                return False
        
        return True