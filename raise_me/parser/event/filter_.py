import json
from typing import Dict, List, Union


class FilterParser:
    @classmethod
    def to_aws_event_pattern(cls, 
                             filters: List[str],
                            ) -> Dict[str, Union[str, List, Dict]]:
        filters = filters.copy()
        for index, f in enumerate(filters):
            sep_index = f.index(':')
            key, val = f[:sep_index], f[sep_index + 1:]
            filters[index] = (key, val)
        return json.dumps({key: val for key, val in filters})
    
    @classmethod
    def to_eventrac_filters(cls, filters: List[str]) -> List[Dict[str, str]]:
        filters = filters.copy()
        for index, f in enumerate(filters):
            sep_index = f.index('=')
            key, val = f[:sep_index], f[sep_index + 1:]
            filters[index] = {'attribute': key, 'value': val}
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