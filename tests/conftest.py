import pathlib
from typing import Dict

import pytest

from raise_me import TESTS_PATH
from raise_me.models import Deployment
from raise_me.parser import ConfigParser, DeploymentParser
from raise_me.wsk import WskClient


@pytest.fixture(scope='session')
def conf_path() -> pathlib.Path:
    return TESTS_PATH / 'raise-config.yaml'


@pytest.fixture(scope='session')
def events_path() -> pathlib.Path:
    return TESTS_PATH / 'raise-events.yaml'


@pytest.fixture(scope='session')
def config(conf_path) -> Dict:
    return ConfigParser.from_yaml(path=conf_path)


@pytest.fixture(scope='session')
def deployment(events_path) -> Deployment:
    return DeploymentParser.from_yaml(path=events_path)


@pytest.fixture
def client(config) -> WskClient:
    return WskClient.from_config(config=config)