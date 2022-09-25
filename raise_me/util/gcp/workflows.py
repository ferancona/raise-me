import base64
import io
import pathlib
from typing import Dict, Union

from ruamel.yaml import YAML

from raise_me.parser import YAMLParser


class GCPWorkflowAdapter:
    def __init__(self,
                 config: Dict,
                 workflow_path: Union[str, pathlib.Path]) -> None:
        self.conf: Dict = config
        self.workflow: Dict = YAMLParser.parse(path=workflow_path)
    
    def to_pulumi_str(self, trigger_name: str) -> str:
        ow_url: str = '{}/api/v1/namespaces/{}'.format(
            self.conf['openwhisk']['endpoint'],
            self.conf['openwhisk']['namespace'],
        )
        for step in self.workflow['main']['steps']:
            if 'init_openwhisk_vars' in step:
                for var in step['init_openwhisk_vars']['assign']:
                    if 'TRIGGER_NAME' in var:
                        var['TRIGGER_NAME'] = trigger_name
                    elif 'OW_URL' in var:
                        var['OW_URL'] = ow_url
            
            if 'fire_openwhisk_trigger' in step:
                ow_auth: Dict[str, str] = self.conf['openwhisk']['auth']
                headers = step['fire_openwhisk_trigger']['args']['headers']
                headers['Authorization'] = 'Basic {}'.format(
                    base64.b64encode(
                        '{}:{}'.format(
                            ow_auth['username'],
                            ow_auth['password'],
                        ).encode()
                    ).decode('ascii'),
                )
        
        yaml = YAML()
        buffer = io.StringIO()
        yaml.dump(data=self.workflow, stream=buffer)
        workflow_str = buffer.getvalue()
        buffer.close()
        return workflow_str