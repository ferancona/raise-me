import pathlib
from typing import Dict, Union

from .yaml_parser import YAMLParser


class ConfigParser:
    @classmethod
    def from_yaml(cls, path: Union[str, pathlib.Path]) -> Dict:
        config: Dict = YAMLParser.parse(path=path)
        if not cls.valid(config=config):
            raise SyntaxError('Configuration file "raise-config.yaml" '
                'malformed.')
        return config
    
    @classmethod
    def valid(cls, config: Dict) -> bool:
        # TODO.
        return True