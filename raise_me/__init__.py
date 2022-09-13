__version__ = '0.0.1'

import pathlib


PROJECT_PATH = pathlib.Path(__file__).resolve().parent.parent
RESOURCES_PATH = PROJECT_PATH / 'resources'

OPENWHISK_CHART_PATH = RESOURCES_PATH / 'helm' / 'openwhisk'
RAISE_DEPLOYMENT_PATH = PROJECT_PATH / 'raise-events.yaml'
RAISE_CONFIG_PATH = PROJECT_PATH / 'raise-config.yaml'
CUSTOM_TARGETS_PATH = RESOURCES_PATH / 'custom-targets'

# Providers available.
PROVIDERS = (
    'aws',
    'gcp',
)
