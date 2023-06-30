
from .element import Element

class ElementPointer(Element):

    def __init__(self,type_name:str):
        super().__init__(type_name)
        self.pointer = True

    def implement_destruction(self,target:str):
        text = f'if({target})' + '{\n'
        text+= f'\tfree({target});\n'
        text+='}\n'
        return text

