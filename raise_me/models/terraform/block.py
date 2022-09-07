from abc import ABC
from dataclasses import dataclass, field
from typing import Any, List, Optional

from . import TerraformBlockType


@dataclass
class Argument:
    key: str
    val: Any


# Perhaps, abstract?
@dataclass
class TerraformBlock:
    type_: TerraformBlockType
    name: str
    logical_name: Optional[str]
    arguments: List["Argument"]=field(default_factory=list)
    blocks: List["TerraformBlock"]=field(default_factory=list)
    
    def __post_init__(self):
        if self.arguments is None: self.arguments = [] 
        if self.blocks is None: self.blocks = [] 
    
    def to_json(self):
        nested = dict()
        for arg in self.arguments:
            nested[arg.key] = arg.val
        for block in self.blocks:
            nested.update(block.to_json())
        
        if self.logical_name is not None:
            nested = {self.logical_name: nested}
        
        return {self.type_.value: {self.name: nested}}


@dataclass
class Resource(TerraformBlock):
    def __init__(self, name: str, logical_name: str, 
                 args: List["Argument"]=None, 
                 blocks: List["TerraformBlock"]=None):
        super().__init__(
            type_=TerraformBlockType.RESOURCE,
            name=name,
            logical_name=logical_name,
            arguments=args,
            blocks=blocks)


@dataclass
class Provider(TerraformBlock):
    def __init__(self, name: str,
                 args: List["Argument"]=None,
                 blocks: List["TerraformBlock"]=None):
        # Todo: Do providers have blocks?
        super().__init__(
            type_=TerraformBlockType.PROVIDER,
            name=name,
            logical_name=None,
            arguments=args,
            blocks=blocks)