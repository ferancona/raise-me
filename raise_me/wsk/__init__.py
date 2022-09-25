from raise_me import PROJECT_PATH
from .client import WskClient

WSK_MODULE_PATH = PROJECT_PATH / 'raise_me' / 'wsk'
HTTP_INVOKER_PATH = WSK_MODULE_PATH / 'http_invoker.py'
HTTP_MEDIATOR_PATH = WSK_MODULE_PATH / 'http_mediator.py'