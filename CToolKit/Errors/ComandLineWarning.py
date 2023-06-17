

class ComandLineWarning(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        text = f'Mensage: {self.message}\n'
        return text

