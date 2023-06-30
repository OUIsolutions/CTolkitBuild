
class Element:

    def __init__(self,type_name:str):
        self.type_name = type_name

    def implement_declaration(self,element_name:str)->str:
        return f'{self.type_name} {element_name};'

    def implement_destruction(self,target:str):
        return ''

    def implement_copy(self,target:str,element_name:str):
        return ''

    def implement_reference(self,target:str,element_name:str):
        text = self.implement_destruction(target)
        return text+ f'{target} = {element_name};'

