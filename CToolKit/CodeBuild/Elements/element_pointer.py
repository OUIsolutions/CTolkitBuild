
from .element import Element

class ElementPointer(Element):

    def implement_destruction(self,target:str):
        return f'free({target});\n'
