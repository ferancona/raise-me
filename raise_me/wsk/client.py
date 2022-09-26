from typing import Dict, Iterator, List

import requests
from requests.models import Response


class WskClient:
    DEFAULT_NS = 'guest'

    def __init__(self,
                 url: str,
                 username: str,
                 password: str,
                 ns: str=None) -> None:
        self.auth = (username, password)
        self.ns = ns if ns else self.DEFAULT_NS
        self.url = '{}/api/v1/namespaces/{}'.format(url, self.ns)

    @classmethod
    def from_config(cls, config: Dict) -> "WskClient":
        ow: Dict = config['openwhisk']
        return WskClient(
            url=ow['endpoint'],
            username=ow['auth']['username'],
            password=ow['auth']['password'],
            ns=ow['namespace'],
        )

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
                'trigger': f'/_/{trigger_name}',
                'action': f'/_/{action_name}',
                'status': 'active',
                'publish': True,
            },
            params={'overwrite': 'true'},
        )
        return r
    
    def delete_action(self, name: str) -> Response:
        url = f'{self.url}/actions/{name}'
        r = requests.delete(url, auth=self.auth)
        return r
    
    def delete_trigger(self, name: str) -> Response:
        url = f'{self.url}/triggers/{name}'
        r = requests.delete(url, auth=self.auth)
        return r
    
    def delete_rule(self, name: str):
        url = f'{self.url}/rules/{name}'
        r = requests.delete(url, auth=self.auth)
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
    
    def list_actions(self, limit=200, skip=0) -> Response:
        """Returns list of action names (max limit: 200)."""
        url = f'{self.url}/actions'
        r = requests.get(
            url,
            auth=self.auth,
            params={
                'limit': limit,
                'skip': skip,
            },
        )
        return r
    
    def list_triggers(self, limit=200, skip=0) -> Response:
        """Returns list of trigger names (max limit: 200)."""
        url = f'{self.url}/triggers'
        r = requests.get(
            url,
            auth=self.auth,
            params={
                'limit': limit,
                'skip': skip,
            },
        )
        return r
    
    def list_rules(self, limit=200, skip=0) -> Response:
        """Returns list of rule names (max limit: 200)."""
        url = f'{self.url}/rules'
        r = requests.get(
            url,
            auth=self.auth,
            params={
                'limit': limit,
                'skip': skip,
            },
        )
        return r
    
    def action_paginator(self) -> "WskPaginator":
        return WskPaginator(client=self, resource='action')
    
    def trigger_paginator(self) -> "WskPaginator":
        return WskPaginator(client=self, resource='trigger')

    def rule_paginator(self) -> "WskPaginator":
        return WskPaginator(client=self, resource='rule')


class WskPaginator:
    def __init__(self, client: WskClient, resource: str) -> None:
        self.client = client

        if resource == 'action':
            self.list_method = self.client.list_actions
        elif resource == 'trigger':
            self.list_method = self.client.list_triggers
        elif resource == 'rule':
            self.list_method = self.client.list_rules
        else:
            raise AttributeError(
                f'No paginator found for resource {resource}.')
    
    def paginate(self) -> Iterator[str]:
        limit = 200
        skip = 0
        response = self.list_method(limit=limit, skip=skip)
        resources = [rsc['name'] for rsc in response.json()]
        while len(resources) == 200:
            for action in resources:
                yield action
            skip += 200
            resources = self.list_method(limit=limit, skip=skip)
        if len(resources) > 0:
            for action in resources:
                yield action