
from typing import Any
from .Elements.convert_type import convert_type
from .Elements.element import Element
from .Elements.element_pointer import ElementPointer
from .ownership import OwnerShip
from .ownership_choices import  *
from .extra import construct_by_default

class StructElement:

    def __init__(
            self,
            name:str,
            element_type:type or Element or ElementPointer,
            ownership_setter: OwnerShip= BY_VALUE,
            ownership_getter: OwnerShip= BY_VALUE_AND_OWNERSHIP,
            private:bool=False,
            private_flag:str='_',
            allow_getter: bool=None,
            allow_setter:bool=None,
            required_at_start:bool=False,
            defaults_to:Any=None,
            ownership_flag:str =None
    ):
        self.name = name

        self.private = private
        self.element_type = convert_type(element_type)
        self.ownership_getter = ownership_getter
        self.ownership_setter = ownership_setter


        self.allow_getter = allow_getter
        if allow_getter is None:
            pass

        self.allow_setter = allow_setter


        self.required_at_start = required_at_start
        self.defaults_to = defaults_to
        self.private_flag = private_flag
        self.ownership_flag =construct_by_default(f'{private_flag}{self.name}_owner')



    def implement_declaration(self):
        text = self.element_type.implement_declaration(self.name)
        if self.ownership.require_ownership_flag:
            text+=f'\n\tbool {self.ownership_flag};'
        return text