
from .primitive_types import *
from .element import Element
from .element_pointer import ElementPointer



def convert_type(type_name:type or Element or ElementPointer)->Element:

    if type_name == str:
        return string_type

    if type_name == int:
        return int_type

    if type_name == bool:
        return bool_type

    if type_name == float:
        return float_type

    return type_name
