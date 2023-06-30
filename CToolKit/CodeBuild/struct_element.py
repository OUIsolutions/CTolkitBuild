
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

            set_flag:str='_set_',
            get_flag:str='_get_',
            by_value_flag:str='_by_value',
            by_reference_flag:str='_by_reference',
            by_ownership_flag:str='_by_ownership',

            private:bool=False,
            private_flag:str='_',


            allow_getter: bool=None,
            allow_setter:bool=None,

            required_at_start:bool=False,
            defaults_to:Any=None,
            ownership_flag:str =None
    ):



        self.private = private
        self.element_type = convert_type(element_type)
        self.ownership_getter = ownership_getter
        self.ownership_setter = ownership_setter
        self.allow_getter = allow_getter
        self.set_flag = set_flag
        self.get_flag = get_flag

        self.by_value_flag = by_value_flag
        self.by_reference_flag = by_reference_flag
        self.by_ownership_flag = by_ownership_flag

        self.required_at_start = required_at_start
        self.defaults_to = defaults_to
        self.private_flag = private_flag

        self.name = name
        if private:
            self.name = private_flag + name
        self.ownership_flag =construct_by_default(f'{private_flag}{self.name}_owner',ownership_flag)
        if allow_getter is None:
            if private:
                self.allow_getter = False

            elif self.element_type.pointer:
                self.allow_getter = True

            else:
                self.allow_getter = False


        self.allow_setter = allow_setter
        if allow_setter is None:

            if self.element_type.pointer:
                self.allow_setter = True

            else:
                self.allow_setter = False



    def _implement_get_args(self,object_self_ref:str)->str:
        return f'({object_self_ref})'

    def _implement_set_args(self,object_self_ref:str)->str:
        return f'({object_self_ref},{self.element_type.type_name} {self.name})'


    def implement_getter_and_setter_declaration(self,method_starter:str,object_self_ref:str)->str:
        get_text = ''

        #getters
        if self.allow_getter:
            get_args = f'{self._implement_get_args(object_self_ref)};'

            if self.ownership_getter.by_value:
                get_text+= f'{self.element_type.type_name} {method_starter}'
                get_text+= f'{self.get_flag}{self.name}{self.by_value_flag}{get_args}\n'


            if self.ownership_getter.by_reference:
                get_text+= f'{self.element_type.type_name} {method_starter}'
                get_text+= f'{self.get_flag}{self.name}{self.by_reference_flag}{get_args}\n'


            if self.ownership_getter.by_ownership:
                get_text+= f'{self.element_type.type_name} {method_starter}'
                get_text+= f'{self.get_flag}{self.name}{self.by_ownership_flag}{get_args}\n'


        set_text = ''
        if self.allow_setter:
            set_args = f'{self._implement_set_args(object_self_ref)};'
            #setter
            if self.ownership_setter.by_value:
                set_text+= f'void {method_starter}{self.set_flag}{self.name}{self.by_value_flag}{set_args}\n'

            if self.ownership_setter.by_reference:
                set_text+= f'void {method_starter}{self.set_flag}{self.name}{self.by_reference_flag}{set_args}\n'

            if self.ownership_setter.by_ownership:
                set_text+= f'void {method_starter}{self.set_flag}{self.name}{self.by_ownership_flag}{set_args}\n'


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