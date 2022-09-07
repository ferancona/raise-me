from dataclasses import dataclass
from typing import List

from . import BlockType
from raise_me.models.terraform.block import TerraformBlock, Argument


@dataclass
class Provider(TerraformBlock):
    def __init__(self, name: str,
                 args: List["Argument"]=None,
                 blocks: List["TerraformBlock"]=None):
        super().__init__(
            type_=BlockType.PROVIDER,
            name=name,
            logical_name=None,
            arguments=args,
            blocks=blocks)