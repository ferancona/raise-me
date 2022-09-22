from .orchestrator import CloudOrchestrator
from .aws import AWSCloud
from .gcp import GCPCloud

from raise_me import RESOURCES_PATH


LAMBDA_RESOURCES_PATH = RESOURCES_PATH / 'aws' / 'lambda'
CLOUDEVENTS_LAYER_PATH = LAMBDA_RESOURCES_PATH / 'layers' \
    / 'cloudevents-1.6.1.zip'
LAMBDA_TRIGGER_PATH = LAMBDA_RESOURCES_PATH / 'functions' \
    / 'openwhisk_trigger.zip'
WORKFLOW_TRIGGER_PATH = RESOURCES_PATH / 'gcp' / 'workflows' \
    / 'openwhisk_trigger.yaml'