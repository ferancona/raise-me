from raise_me.exceptions import UnrecognizedTargetType

from raise_me.models.event.target import CustomTarget, EventTarget, HttpTarget


class EventTargetParser:
    VALID_KEYS = (
        'http', 
        'custom',
    )

    @classmethod
    def from_dict(cls, target: dict) -> EventTarget:
        t_type = target.keys()[0]
        if t_type == 'http':
            return HttpTargetParser.from_dict(http_target=target[t_type])
        elif t_type == 'custom':
            return CustomTargetParser.from_dict(custom_target=target[t_type])
            
        raise UnrecognizedTargetType(f'{target}')

    @classmethod
    def valid(cls, target: dict) -> bool:
        """Validates targets' syntax in terms of key values and types."""
        if isinstance(target, dict) and \
                len(target.keys()) == 1 and \
                target.keys()[0] in cls.VALID_KEYS:
            t_type = target.keys()[0]

            if not isinstance(target[t_type], dict):
                return False

            valid_target = HttpTargetParser.valid(http_target=target[t_type]) \
                if t_type == 'http' \
                else CustomTargetParser.valid(custom_target=target[t_type])
            
            if not valid_target:
                return False
        else:
            return False
        return True


class HttpTargetParser:
    VALID_KEYS = (
        'method', 
        'url',
    )

    @classmethod
    def from_dict(cls, http_target: dict) -> HttpTarget:
        return HttpTarget(
            method=http_target['method'],
            url=http_target['url'],
        )

    @classmethod
    def valid(cls, http_target: dict) -> bool:
        valid_keys = 'method' in http_target and \
            'url' in http_target and \
            all((key in cls.VALID_KEYS for key in http_target.keys()))
        
        if not valid_keys:
            return False
        if not isinstance(http_target['method'], str):
            return False
        if not isinstance(http_target['url'], str):
            return False
        return True


class CustomTargetParser:
    VALID_KEYS = (
        'filename',
    )

    @classmethod
    def from_dict(cls, custom_target: dict) -> CustomTarget:
        return CustomTarget(
            filename=custom_target['filename'],
        )

    @classmethod
    def valid(cls, custom_target: dict) -> bool:
        if 'filename' not in custom_target:
            return False
        if not isinstance(custom_target['filename'], str):
            return False
        return True