
from typing import Any
from .Elements.convert_type import convert_type
from .Elements.element import Element
from .Elements.element_pointer import ElementPointer
from .ownership import OwnerShip
from .ownership_choices import  *
class StructElement:


    def __init__(
            self,
            name:str,
            element_type:type or Element or ElementPointer,
            ownership: OwnerShip = None,
            required_at_start:bool=False,
            defaults_to:Any=None,
            ownership_flag:str =None
    ):
        self.name = name
        self.element_type = convert_type(element_type)
        self.required_at_start = required_at_start
        self.defaults_to = defaults_to

        if ownership is None:
            self.ownership = by_value

        self.ownership_flag = ownership_flag
        if ownership_flag is None and self.ownership.require_ownership_flag:
            self.ownership_flag = f'_{self.name}_owner'

    def implement_declaration(self):
        text = self.element_type.implement_declaration(self.name) + '\n'
        if self.ownership.require_ownership_flag:
            text+=f'\tbool {self.ownership_flag};'
        return text