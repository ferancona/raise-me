import uuid
from dataclasses import dataclass

import pytest

from raise_me.wsk import WskClient, WskPaginator


@dataclass
class Action:
    name: str
    runtime: str
    code: str
    main: str


@pytest.fixture
def action_name():
    return f'a-beautiful-action-name-{uuid.uuid4()}'


@pytest.fixture
def trigger_name():
    return f'a-beautiful-trigger-name-{uuid.uuid4()}'


@pytest.fixture
def rule_name():
    return f'a-beautiful-rule-name-{uuid.uuid4()}'


@pytest.fixture
def action(action_name) -> Action:
    return Action(
        name=action_name,
        runtime='python:3',
        code='def main(args):\n    return {}',
        main='main',
    )


@pytest.fixture
def action_resource(client: WskClient, action: Action):
    _ = client.create_action(
        name=action.name,
        runtime=action.runtime,
        code=action.code,
        main=action.name,
    )
    yield action
    _ = client.delete_action(name=action.name)
    
@pytest.fixture
def trigger_resource(client: WskClient, trigger_name):
    _ = client.create_trigger(name=trigger_name)
    yield trigger_name
    _ = client.delete_trigger(name=trigger_name)


@pytest.fixture
def rule_resource(client: WskClient,
                  action_resource: Action,
                  trigger_resource: str,
                  rule_name):
    _ = client.create_rule(
        name=rule_name,
        trigger_name=trigger_resource,
        action_name=action_resource.name,
    )
    yield rule_name
    _ = client.delete_rule(name=rule_name)


@pytest.mark.client
class TestWskClient:
    def test_list_actions(self, client: WskClient):
        res = client.list_actions()
        assert res.status_code == 200
    
    def test_list_triggers(self, client: WskClient):
        res = client.list_triggers()
        assert res.status_code == 200
    
    def test_list_rules(self, client: WskClient):
        res = client.list_rules()
        assert res.status_code == 200
    
    def test_create_delete_action(self, client: WskClient, action: Action):
        res_create = client.create_action(
            name=action.name,
            runtime=action.runtime,
            code=action.code,
            main=action.name,
        )
        res_delete = client.delete_action(name=action.name)
        assert res_create.status_code == 200 and \
            res_create.json()['name'] == action.name
        assert res_delete.status_code == 200
    
    def test_create_delete_trigger(self, client: WskClient, trigger_name):
        res_create = client.create_trigger(name=trigger_name)
        res_delete = client.delete_trigger(name=trigger_name)
        assert res_create.status_code == 200 and \
            res_create.json()['name'] == trigger_name
        assert res_delete.status_code == 200

    def test_create_delete_rule(self,
                                client: WskClient,
                                action_resource: Action,
                                trigger_resource: str,
                                rule_name):
        res_create = client.create_rule(
            name=rule_name,
            trigger_name=trigger_resource,
            action_name=action_resource.name,
        )
        res_delete = client.delete_rule(name=rule_name)
        assert res_create.status_code == 200 and \
            res_create.json()['name'] == rule_name
        assert res_delete.status_code == 200


@pytest.mark.paginator
class TestWskPaginator:
    @pytest.fixture
    def action_paginator(self, client: WskClient):
        return WskPaginator(client=client, resource='action')
    
    @pytest.fixture
    def trigger_paginator(self, client: WskClient):
        return WskPaginator(client=client, resource='trigger')
    
    @pytest.fixture
    def rule_paginator(self, client: WskClient):
        return WskPaginator(client=client, resource='rule')
    
    def test_paginate_actions(self,
                              action_resource: Action,
                              action_paginator: WskPaginator):
        resource_found = False
        for action in action_paginator.paginate():
            if action == action_resource.name:
                resource_found = True
        assert resource_found
    
    def test_paginate_triggers(self,
                              trigger_resource: str,
                              trigger_paginator: WskPaginator):
        resource_found = False
        for action in trigger_paginator.paginate():
            if action == trigger_resource:
                resource_found = True
        assert resource_found
    
    def test_paginate_rules(self,
                              rule_resource: str,
                              rule_paginator: WskPaginator):
        resource_found = False
        for action in rule_paginator.paginate():
            if action == rule_resource:
                resource_found = True
        assert resource_found