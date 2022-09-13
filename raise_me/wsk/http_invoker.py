import requests
from typing import Dict


def main(args: dict) -> dict:
    event: Dict = args.get('event')
    http_target: Dict = args.get('http_target')

    http_method: str = http_target.get('method')
    url: str = http_target.get('url')
    
    if http_method == 'get':
        r = requests.get(url)
    else: # post
        r = requests.post(url, json=event)
    
    return r.json()