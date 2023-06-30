
from .Elements.convert_type import convert_type
from .Elements.element import Element
from .Elements.element_pointer import ElementPointer


class StructElement:


    def __init__(
            self,
            name:str,
            element_type:type or Element or ElementPointer,
            by_value:bool=True,
            by_reference:bool=False,
            by_ownership:bool=False
    ):
        self.name = name
        self.element_type = convert_type(element_type)
        self.by_value = by_value
        self.by_reference = by_reference
        self.by_ownership = by_ownership

        total_elements = 0
        if by_value:
            total_elements+=1

        if by_reference:
            total_elements+=1

        if by_ownership:
            total_elements+=1

        assert total_elements > 0

        self.require_ownership_flag = False
        if total_elements > 1:
            self.require_ownership_flag = True

    def implement_declaration(self):
        return self.element_type.implement_declaration(self.name)


