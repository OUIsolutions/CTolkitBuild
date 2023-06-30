from element_pointer import ElementPointer


class StringType(ElementPointer):

    def implement_copy(self,target:str,element_name:str):
        text = self.implement_destruction(target)
        return text + f'{target} = strdup({element_name})'


