class BaseResource():
    def __init__(self):
        self.type = ''
        self.name = ''
    
    def get_identifier(self) -> str:
        return f'{self.type}.{self.name}'