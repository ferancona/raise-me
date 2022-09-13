from typing import Dict, List

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
        url = f'{self.url}/actions/{name}'
        r = requests.put(
            url,
            auth=self.auth,
            json={
                'namespace': self.ns,
                'name': name,
                'exec': {
                    'kind': runtime,
                    'code': code,
                    'main': main,
                },
                'publish': True,
            },
            params={'overwrite': 'true'},
        )
        return r

    def create_trigger(self, name: str) -> Response:
        url = f'{self.url}/triggers/{name}'
        r = requests.put(
            url,
            auth=self.auth,
            json={
                'namespace': self.ns,
                'name': name,
                'publish': True,
            },
            params={'overwrite': 'true'},
        )
        return r

    def create_rule(self,
                    name: str,
                    trigger_name: str,
                    action_name: str) -> Response:
        url = f'{self.url}/rules/{name}'
        r = requests.put(
            url,
            auth=self.auth,
            json={
                'name': name,
                'trigger': trigger_name,
                'action': action_name,
                'status': 'active',
                'publish': True,
            },
            params={'overwrite': 'true'},
        )
        return r
    
    def delete_action(self, name: str) -> Response:
        url = f'{self.url}/actions/{name}'
        r = requests.delete(url)
        return r
    
    def delete_trigger(self, name: str) -> Response:
        url = f'{self.url}/triggers/{name}'
        r = requests.delete(url)
        return r
    
    def delete_rule(self, name: str):
        url = f'{self.url}/rules/{name}'
        r = requests.delete(url)
        return r

    def fire_trigger(self, name: str, args: Dict=None) -> Response:
        args = args if args else dict()
        url = f'{self.url}/triggers/{name}'
        r = requests.post(
            url,
            auth=self.auth,
            json=args,
            params={
                'blocking': False,
                'result': False,
            },
        )
        return r
    
    def invoke_action(self, name: str, args: Dict=None) -> Response:
        args = args if args else dict()
        url = f'{self.url}/actions/{name}'
        r = requests.post(
            url,
            auth=self.auth,
            json=args,
            params={
                'blocking': False,
                'result': False,
            },
        )
        return r
    
    def list_actions(self, limit=200) -> List[str]:
        """Returns list of action names (max_size: 200)."""
        # TODO: test
        url = f'{self.url}/actions'
        r = requests.get(
            url,
            auth=self.auth,
            params={
                'limit': limit,
            },
        )
        return [action['name'] for action in r.json()]
    
    def list_triggers(self, limit=200) -> List[str]:
        """Returns list of trigger names (max_size: 200)."""
        # TODO: test
        url = f'{self.url}/triggers'
        r = requests.get(
            url,
            auth=self.auth,
            params={
                'limit': 200,
            },
        )
        return [trigger['name'] for trigger in r.json()]
    
    def list_rules(self, limit=200) -> List[str]:
        """Returns list of rule names (max_size: 200)."""
        # TODO: test
        url = f'{self.url}/rules'
        r = requests.get(
            url,
            auth=self.auth,
            params={
                'limit': 200,
            },
        )
        return [rule['name'] for rule in r.json()]