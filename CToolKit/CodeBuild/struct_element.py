
from .Elements.convert_type import convert_type
from .Elements.element import Element
from .Elements.element_pointer import ElementPointer


class StructElement:


    def __init__(
            self,
            name:str,
            element_type:type or Element or ElementPointer,
            required_at_start:bool=False,
            by_value:bool=True,
            by_reference:bool=False,
            by_ownership:bool=False,
            ownership_flag:str =None
    ):
        self.name = name
        self.element_type = convert_type(element_type)
        self.required_at_start = required_at_start
        self.by_value = by_value
        self.by_reference = by_reference
        self.by_ownership = by_ownership
        self.ownership_flag = ownership_flag

        if ownership_flag is None:
            self.ownership_flag = f'_{self.name}_owner'

        total_elements = 0
        if by_value:
            total_elements+=1

        if by_reference:
            total_elements+=1

        if by_ownership:
            total_elements+=1


        self.require_ownership_flag = False
        if total_elements > 1:
            self.require_ownership_flag = True


    def implement_declaration(self):
        text = self.element_type.implement_declaration(self.name) + '\n'
        if self.require_ownership_flag:
            text+=f'\tbool {self.ownership_flag};'
        return text