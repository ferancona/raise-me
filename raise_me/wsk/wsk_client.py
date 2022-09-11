from typing import Dict
import requests
from requests.models import Response

class WskClient:
    DEFAULT_NS = '_'

    def __init__(self,
                 api_host: str,
                 username: str,
                 password: str,
                 ns: str=None,
                 https: bool=False) -> None:
        self.auth = (username, password)
        self.ns = ns if ns else self.DEFAULT_NS
        self.url = '{}://{}/api/v1/namespaces/{}'.format(
            "https" if https else "http", api_host, self.ns)

    def create_action(self, 
                      name: str, 
                      runtime: str, 
                      code: str, 
                      main: str=None) -> Response:
        main = main if main else 'main'
        url = f'{self.url}/actions/{name}?overwrite=true'
        r = requests.put(
            url,
            auth=self.auth,
            data={
                'namespace': self.ns,
                'name': name,
                'exec': {
                    'kind': runtime,
                    'code': code,
                    'main': main,
                },
                'publish': True,
            }
        )
        return r
    
    def invoke_action(self, name: str, args: Dict=None) -> Response:
        url = f'{self.url}/actions/{name}'
        r = requests.post(
            url,
            auth=self.auth,
            data={
                'actionName': name,
                'namespace': self.ns,
                'payload': args,
                'blocking': False,
                'result': False,
            }
        )
        return r