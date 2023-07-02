from .struct_element import StructElement
from typing import List


class Struct:

    def __init__(self,
                 type_name: str,
                 elements: List[StructElement],

                 initializer_name='@typename@new',
                 destructor_name='@typename@free',

                 implement_represent_method=True,
                 represent_method_name='@typename@represent',

                 implement_copy_method=True,
                 copy_method_name='@typename@copy',

                 allow_function_pointers: bool = False,


                 object_reference: str = 'self'
                 ):

        self.type_name = type_name
        self.elements = elements
        self.allow_function_pointers = allow_function_pointers
        self.object_reference = object_reference

        self.destructor_name = destructor_name.replace('@typename@',type_name)
        self.initializer_name = initializer_name.replace('@typename@',type_name)
        self.copy_method_name = copy_method_name.replace('@typename@',type_name)

        self.implement_copy_method = implement_copy_method
        self.implement_represent_method = implement_represent_method
        self.represent_method_name = represent_method_name.replace('@typename@',type_name)


    def _implement_self_ref(self)->str:
        return f'{self.type_name}* {self.object_reference}'

    def implement_self_type(self)->str:
        return f'{self.type_name}*'


    def _implement_struct_declaration(self):
        text = f'typedef struct {self.type_name}' + '{\n\n'
        for i in self.elements:
            text += f'\t{i.implement_declaration()}\n'

        text += '\n}' + f'{self.type_name};\n\n'
        return text

    def generate_declaration(self, output: str = None) -> str:

        # struct declaration
        text = self._implement_struct_declaration()

        # constructr method
        text += f'{self.implement_self_type()} {self.initializer_name}();\n\n'


        if self.implement_copy_method:
            text += f'{self.implement_self_type()}  {self.copy_method_name}({self._implement_self_ref()});\n\n'


        # desctructor method
        text += f'void {self.destructor_name}({self._implement_self_ref()});\n\n'

        if output:
            save_file(text, output)


        return text
