class BaseResource():
    def __init__(self):
        self.projectType = None
        self.type = None
        self.name = ''
    
    def get_identifier(self) -> str:
        return f'{self.type.value}.{self.name}' if self.name else self.type.value