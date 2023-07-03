

class FolderPressetError(Exception):
    
    def __init__(self, mensage:str) -> None:
        self.mensage = mensage
        
        