import json
import os
import requests

from cloudevents.http import CloudEvent
from cloudevents.conversion import to_structured


# TODO: Use SecretsManager instead of AUTH variable.


AUTH = (os.environ.get('OW_USER'), os.environ.get('OW_PASS'))
OW_URL = os.environ.get('OW_URL')
TRIGGER_NAME = os.environ.get('TRIGGER_NAME')


def handler(event, context):
    attributes = {
        "type": event['detail-type'].replace(" ", "."),
        "source": event['source'],
        "subject": event['source'],
        "id": event['id'],
        "time": event['time'],
    }
    data = {
        "account": event['account'],
        "region": event['region'],
        "resources": event['resources'],
        "detail": event['detail'],
    }

    event = CloudEvent(attributes, data)
    _, body = to_structured(event)
    body = {'event': json.loads(body.decode())}
    print(event)

    url = f'{OW_URL}/triggers/{TRIGGER_NAME}'
    res = requests.post(
        url,
        auth=AUTH,
        json=body,
        params={
            'blocking': False,
            'result': False,
        },
    )
    
    return {
        'statusCode': res.status_code,
        'body': {
            'ow_response': res.json(),
        },
    }