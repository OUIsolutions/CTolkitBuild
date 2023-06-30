from .file_saving import save_file
from .struct_element import StructElement
from typing import List


class Struct:

    def __init__(self,
                 name: str,
                 elements: List[StructElement],
                 initializer_name: str = None,
                 destructor_name: str = None,
                 allow_function_pointers: bool = False,
                 implement_copy_method: bool = False,
                 copy_method_name: str = None,
                 self_name: str = 'self'
                 ):

        self.name = name
        self.allow_function_pointers = allow_function_pointers
        self.self_name = self_name
        self.initializer_name = initializer_name
        self.elements = elements

        if initializer_name is None:
            self.initializer_name = f'{name}_new'

        self.destructor_name = destructor_name

        if destructor_name is None:
            self.destructor_name = f'{name}_free'

        self.copy_method_name = copy_method_name
        self.implement_copy_method = implement_copy_method

        if implement_copy_method and copy_method_name is None:
            self.copy_method_name = f'{name}_copy'

    def generate_declaration(self, output: str = None) -> str:

        # struct declaration
        text = f'typedef struct {self.name}' + '{\n\n'
        for i in self.elements:
            text += f'\t{i.implement_declaration()}\n'

        text += '\n}' + f'{self.name};\n\n'

        # constructr method
        text += f'{self.name} * {self.initializer_name}();\n\n'

        if self.implement_copy_method:
            text += f'{self.name} * {self.copy_method_name}({self.name} * {self.self_name});\n\n'

        # desctructor method
        text += f'void {self.destructor_name}({self.name}* {self.self_name});\n\n'

        if output:
            save_file(text, output)

        return text
