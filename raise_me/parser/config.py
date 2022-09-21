import pathlib
from typing import Dict, Union

from ruamel.yaml import YAML


class ConfigParser:
    @classmethod
    def from_yaml(cls, path: Union[str, pathlib.Path]) -> Dict:
        path = pathlib.Path(path).resolve()
        parser = YAML(typ='safe')
        try:
            with open(path, 'r') as f:
                config: Dict = parser.load(f.read())
        except Exception as err:
            raise err

        if not cls.valid(config=config):
            raise SyntaxError('Configuration file "raise-config.yaml" '
                'malformed.')
        
        return config
    
    @classmethod
    def valid(cls, config: Dict) -> bool:
        # TODO.
        ...