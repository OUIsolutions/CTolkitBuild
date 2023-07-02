from .struct_element import StructElement
from .extra import  save_file
from typing import List


class Struct:

    def __init__(self,
                 name: str,
                 elements: List[StructElement],

                 initializer_name='@name@new',
                 destructor_name='@name@free',

                 implement_represent_method=True,
                 represent_method_name='@name@represent',

                 implement_copy_method=True,
                 copy_method_name='@name@copy',

                 allow_function_pointers: bool = False,


                 object_reference: str = 'self'
                 ):

        self.name = name
        self.elements = elements
        self.allow_function_pointers = allow_function_pointers
        self.object_reference = object_reference

        self.destructor_name = destructor_name.replace('@name@',name)
        self.initializer_name = initializer_name.replace('@name@',name)
        self.copy_method_name = copy_method_name.replace('@name@',name)

        self.implement_copy_method = implement_copy_method
        self.implement_represent_method = implement_represent_method
        self.represent_method_name = represent_method_name.replace('@name@',name)


    def _implement_self_ref(self)->str:
        return f'{self.name}* {self.object_reference}'

    def implement_self_type(self)->str:
        return f'{self.name}*'


    def _implement_struct_declaration(self):
        text = f'typedef struct {self.name}' + '{\n\n'
        for i in self.elements:
            text += f'\t{i.implement_declaration()}\n'

        text += '\n}' + f'{self.name};\n\n'
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
