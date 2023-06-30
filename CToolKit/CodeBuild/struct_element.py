
from typing import Any
from .Elements.convert_type import convert_type
from .Elements.element import Element
from .Elements.element_pointer import ElementPointer
from .ownership import OwnerShip
from .ownership_choices import  *
from .extra import construct_by_default

class StructElement:

    def __init__(
            self,
            name:str,
            element_type:type or Element or ElementPointer,
            ownership_setter: OwnerShip= BY_VALUE,
            ownership_getter: OwnerShip= BY_VALUE_AND_REFERENCE,

            set_flag:str='_set',
            get_flag:str='_get',
            by_value_flag:str='_by_value',
            by_reference_flag:str='by_reference',
            by_ownership_flag:str='by_ownership',

            private:bool=False,
            private_flag:str='__',


            allow_getter: bool=None,
            allow_setter:bool=None,

            required_at_start:bool=False,
            defaults_to:Any=None,
            ownership_flag:str =None
    ):

        self.name = name
        if private:
            self.name = private_flag + name

        self.private = private
        self.element_type = convert_type(element_type)
        self.ownership_getter = ownership_getter
        self.ownership_setter = ownership_setter


        self.allow_getter = allow_getter

        if allow_getter is None:
            if private:
                self.allow_getter = False

            elif element_type.pointer:
                self.allow_getter = True

            else:
                self.allow_getter = False


        if allow_setter is None:

            if element_type.pointer:
                self.allow_setter = True
            else:
                self.allow_setter = False


        self.allow_setter = allow_setter

        self.set_flag = set_flag
        self.get_flag = get_flag

        self.by_value_flag = by_value_flag
        self.by_reference_flag = by_reference_flag
        self.by_ownership_flag = by_ownership_flag

        self.required_at_start = required_at_start
        self.defaults_to = defaults_to
        self.private_flag = private_flag
        self.ownership_flag =construct_by_default(f'{private_flag}{self.name}_owner',ownership_flag)









    def implement_getter_and_setter_declaration(self,method_starter:str,object_self_ref:str)->str:
        get_text = ''

        get_args =f'({object_self_ref});'
        #getters
        if self.ownership_getter.by_value:
            get_text+= f'{self.element_type.type_name} {method_starter}'
            get_text+= f'{self.get_flag}{self.by_value_flag}{get_args}\n'


        if self.ownership_getter.by_reference:
            get_text+= f'{self.element_type.type_name} {method_starter}'
            get_text+= f'{self.get_flag}{self.by_reference_flag}{get_args}\n'


        if self.ownership_getter.by_ownership:
            get_text+= f'{self.element_type.type_name} {method_starter}'
            get_text+= f'{self.get_flag}{self.by_ownership_flag}{get_args}\n'


        set_text = ''
        set_args = f'({object_self_ref},{self.element_type.type_name} {self.name});'
        #setter
        if self.ownership_setter.by_value:
            set_text+= f'void {method_starter}{self.set_flag}{self.by_value_flag}{set_args}'


        if self.ownership_setter.by_reference:
            set_text+= f'void {method_starter}{self.set_flag}{self.by_reference_flag}{set_args}'

        if self.ownership_setter.by_ownership:
            set_text+= f'void {method_starter}{self.set_flag}{self.by_ownership_flag}{set_args}'

        text = ''
        if get_text:
            text+=get_text+'\n'
        if set_text:
            text+=set_text+'\n'
        return text

    def implement_declaration(self):
        text = self.element_type.implement_declaration(self.name)
        if self.ownership_setter.require_ownership_flag:
            text+=f'\n\tbool {self.ownership_flag};'
        return text