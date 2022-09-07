from dataclasses import dataclass
from typing import List

from . import BlockType
from raise_me.models.terraform.block import TerraformBlock, Argument


@dataclass
class Resource(TerraformBlock):
    def __init__(self, name: str, logical_name: str, 
                 args: List["Argument"]=None, 
                 blocks: List["TerraformBlock"]=None):
        super().__init__(
            type_=BlockType.RESOURCE,
            name=name,
            logical_name=logical_name,
            arguments=args,
            blocks=blocks)