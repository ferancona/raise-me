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
        if 'openwhisk' not in config:
            return False
        
        ow = config['openwhisk']
        if 'namespace' not in ow or 'endpoint' not in ow or 'auth' not in ow:
            return False
        
        auth = ow['auth']
        if 'username' not in auth or 'password' not in auth:
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
        if 'gcp' not in config:
            return False
        
        gcp = config['gcp']
        if 'project-id' not in gcp or 'region' not in gcp:
            return False
        
        if len(gcp['project-id'].strip()) == 0 or \
                len(gcp['region'].strip()) == 0:
            return False
        return True