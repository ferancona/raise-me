__version__ = '0.0.1'

import pathlib


PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
RESOURCES_PATH = PROJECT_PATH / 'resources'
TESTS_PATH = PROJECT_PATH / 'tests'

RAISE_DEPLOYMENT_PATH = PROJECT_PATH / 'raise-events.yaml'
RAISE_CONFIG_PATH = PROJECT_PATH / 'raise-config.yaml'

# Providers available.
PROVIDERS = (
    'aws',
    'gcp',
)
