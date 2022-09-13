import os
import requests
from typing import Dict, List

# Variable values added when mediator action deployed.
HTTP_TARGETS: List[Dict]
AUTH: tuple


def main(args: dict) -> dict:
    event: Dict = args.get('event')

    apihost = os.getenv('__OW_API_HOST')
    ns = os.getenv('__OW_NAMESPACE')
    invoker_name = 'raise-http-invoker'
    invoker_url = '{}:443/api/v1/namespaces/{}/actions/{}'.format(
        apihost, ns, invoker_name)
    
    for target in HTTP_TARGETS:
        # Invoke 'raise-http-invoker' action.
        _ = requests.post(
            invoker_url,
            auth=AUTH,
            json={
                'event': event,
                'http_target': target,
            },
            params={
                'blocking': False,
                'result': False,
            },
        )

    return {}