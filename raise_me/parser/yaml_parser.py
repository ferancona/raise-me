import pathlib
from typing import Dict, Union

from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError


class YAMLParser:
    @classmethod
    def parse(cls,  path: Union[str, pathlib.Path]) -> Dict:
        path = pathlib.Path(path).resolve()
        parser = YAML(typ='safe')
        try:
            with open(path, 'r') as f:
                yaml_: Dict = parser.load(f.read())
        except DuplicateKeyError as err:
            # Log.
            raise err
        
        return yaml_