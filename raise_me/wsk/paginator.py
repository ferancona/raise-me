from typing import Iterator

from .client import WskClient


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
        resources = self.list_method(limit=limit, skip=skip)
        while len(resources) == 200:
            for action in resources:
                yield action
            skip += 200
            resources = self.list_method(limit=limit, skip=skip)
        if len(resources) > 0:
            for action in resources:
                yield action