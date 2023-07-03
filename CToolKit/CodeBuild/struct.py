from .struct_element import StructElement
from .extra import  save_file
from typing import List


class Struct:

    def __init__(self,
                 name: str,
                 elements: List[StructElement],

                 initializer_name='@name@_new',
                 destructor_name='@name@_free',

                 implement_represent_method=True,
                 represent_method_name='@name@_represent',

                 implement_copy_method=True,
                 copy_method_name='@name@_copy',

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


    
    def generate_declaration(self, output: str = None) -> str:

        # struct declaration
        text = ''


        if output:
            save_file(text, output)



        return text
