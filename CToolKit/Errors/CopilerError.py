
class CompilationError(Exception):
    def __init__(self, message:str, status_code:int,only_warning: bool):
        self.status_code = status_code
        self.only_warning = only_warning
        self.message = message

    def __str__(self):
        text =  f'Mensage: {self.message}\n'
        text += f'Only Warning : {self.only_warning}\n'
        text += f'Status Code: {self.status_code}\n'
        return text

