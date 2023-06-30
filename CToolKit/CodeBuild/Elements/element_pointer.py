
from .element import Element

class ElementPointer(Element):

    def implement_destruction(self,target:str):
        text = f'if({target})' + '{\n'
        text+= f'\tfree({target});\n'
        text+='}\n'
        return text

