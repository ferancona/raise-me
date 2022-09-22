from .openwhisk_builder import OpenwhiskBuilder

from raise_me import RAISE_CONFIG_PATH, RESOURCES_PATH
from raise_me.parser import ConfigParser


LAMBDA_RESOURCES_PATH = RESOURCES_PATH / 'aws' / 'lambda'
CLOUDEVENTS_LAYER_PATH = LAMBDA_RESOURCES_PATH / 'layers' \
    / 'cloudevents-1.6.1.zip'
LAMBDA_TRIGGER_PATH = LAMBDA_RESOURCES_PATH / 'functions' \
    / 'openwhisk_trigger.zip'
WORKFLOW_TRIGGER_PATH = RESOURCES_PATH / 'gcp' / 'workflows' \
    / 'openwhisk_trigger.yaml'

conf = ConfigParser.from_yaml(path=RAISE_CONFIG_PATH)
EVENT_BUS_NAME = conf['aws']['event-bus-name']
OW_ENDPOINT = conf['openwhisk']['endpoint']
OW_USERNAME = conf['auth']['username']
OW_PASSWORD = conf['auth']['password']