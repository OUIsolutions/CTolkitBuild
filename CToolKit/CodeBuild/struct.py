from .extra import save_file, construct_by_default
from .struct_element import StructElement
from typing import List


class Struct:

    def __init__(self,
                 type_name: str,
                 elements: List[StructElement],
                 initializer_name: str = None,
                 starter_method_name:str=None,
                 destructor_name: str = None,
                 allow_function_pointers: bool = False,
                 implement_copy_method: bool = True,
                 copy_method_name: str = None,
                 implement_represent_method:bool = True,
                 represent_method_name:str=None,
                 self_name: str = 'self'
                 ):

        self.type_name = type_name
        self.elements = elements
        self.allow_function_pointers = allow_function_pointers
        self.self_name = self_name
        self.destructor_name = construct_by_default(f'{type_name}_free',destructor_name)
        self.initializer_name = construct_by_default(f'{type_name}_new',initializer_name)
        self.copy_method_name = construct_by_default( f'{type_name}_copy',copy_method_name)
        self.starter_method_name = construct_by_default(type_name,starter_method_name)
        self.implement_copy_method = implement_copy_method
        self.implement_represent_method = implement_represent_method
        self.represent_method_name = construct_by_default(f'{type_name}_represent',represent_method_name)



    def _implement_self_ref(self)->str:
        return f'{self.type_name} * {self.self_name}'

    def implement_self_type(self)->str:
        return f'{self.type_name} *'


    def generate_declaration(self, output: str = None) -> str:

        # struct declaration
        text = f'typedef struct {self.type_name}' + '{\n\n'
        for i in self.elements:
            text += f'\t{i.implement_declaration()}\n'

        text += '\n}' + f'{self.type_name};\n\n'

        # constructr method
        text += f'{self.type_name} * {self.initializer_name}();\n\n'

        for i in self.elements:
            text+= i.implement_getter_and_setter_declaration(self.starter_method_name,self._implement_self_ref())


        if self.implement_copy_method:
            text += f'{self.implement_self_type()}  {self.copy_method_name}({self._implement_self_ref()});\n\n'


        # desctructor method
        text += f'void {self.destructor_name}({self._implement_self_ref()});\n\n'

        if output:
            save_file(text, output)

        return text
