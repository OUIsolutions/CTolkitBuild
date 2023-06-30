
from .primitive_types import *
from .element import Element
from .element_pointer import ElementPointer



def convert_type(type_name:type or Element or ElementPointer)->Element:

    if type_name == str:
        return STRING

    if type_name == int:
        return INT

    if type_name == bool:
        return BOOL

    if type_name == float:
        return FLOAT

    return type_name
