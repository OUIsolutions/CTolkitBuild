
from typing import Any
from .Elements.convert_type import convert_type
from .Elements.element import Element
from .Elements.element_pointer import ElementPointer
from .ownership import OwnerShip
from .ownership_choices import  *

class StructElement:

    def __init__(
            self,
            name: str,
            element_type:type or Element or ElementPointer,
            ownership_setter: OwnerShip = BY_VALUE,
            ownership_getter: OwnerShip = BY_VALUE_AND_REFERENCE,
            set_flag='_set_',
            get_flag='_get_',
            by_value_flag='_by_value',
            by_reference_flag='_by_reference',
            by_ownership_flag='_by_ownership',
            private=False,
            private_flag='_',

            allow_getter: bool=None,
            allow_setter:bool=None,

            required_at_start=False,
            defaults_to:Any=None,
            ownership_flag='@name@_@private_flag@_owner'
    ):



        self.private = private
        self.element_type = convert_type(element_type)
        self.ownership_getter = ownership_getter
        self.ownership_setter = ownership_setter
        self.allow_getter = allow_getter
        self.set_flag = set_flag
        self.get_flag = get_flag

        self.by_value_flag = by_value_flag
        self.by_reference_flag = by_reference_flag
        self.by_ownership_flag = by_ownership_flag

        self.required_at_start = required_at_start
        self.defaults_to = defaults_to
        self.private_flag = private_flag

        self.name = name
        if private:
            self.name = private_flag + name
        self.ownership_flag =ownership_flag.replace('@name@',name).replace('@private_flag@',private_flag)
        if allow_getter is None:
            if private:
                self.allow_getter = False

            elif self.element_type.pointer:
                self.allow_getter = True

            else:
                self.allow_getter = False


        self.allow_setter = allow_setter
        if allow_setter is None:

            if self.element_type.pointer:
                self.allow_setter = True

            else:
                self.allow_setter = False


