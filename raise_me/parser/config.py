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
        if not cls.valid_openwhisk(config=config):
            return False
        if not cls.valid_gcp(config=config):
            return False
        return True
    
    @classmethod
    def valid_openwhisk(cls, config: Dict) -> bool:
        if 'openwhisk' not in config or \
                not isinstance(config['openwhisk'], dict):
            return False
        
        ow = config['openwhisk']
        if 'namespace' not in ow or 'endpoint' not in ow or 'auth' not in ow:
            return False
        
        if not isinstance(ow['namespace'], str) or \
                not isinstance(ow['endpoint'], str) or \
                not isinstance(ow['auth'], dict):
            return False
        
        auth = ow['auth']
        if 'username' not in auth or 'password' not in auth:
            return False
        
        if not isinstance(auth['username'], str) or \
                not isinstance(auth['password'], str):
            return False
        
        if len(ow['namespace'].strip()) == 0 or \
                len(ow['endpoint'].strip()) == 0:
            return False
        
        if len(auth['username'].strip()) == 0 or \
                len(auth['password'].strip()) == 0:
            return False
        return True
    
    @classmethod
    def valid_gcp(cls, config: Dict) -> bool:
        if 'gcp' not in config or \
                not isinstance(config['gcp'], dict):
            return False
        
        gcp = config['gcp']
        if 'project-id' not in gcp or 'region' not in gcp:
            return False

        if not isinstance(gcp['project-id'], str) or \
                not isinstance(gcp['region'], str):
            return False
        
        if len(gcp['project-id'].strip()) == 0 or \
                len(gcp['region'].strip()) == 0:
            return False
        return True