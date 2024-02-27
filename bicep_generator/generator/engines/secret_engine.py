from .base_engine import BaseEngine

# Secret engine interface
class SecretEngine(BaseEngine):
    def __init__(self, connector):
        super().__init__(connector)
    
    def generate_variables(self):
        self.set_variables()
        return super().generate_variables()
    
    def set_module_param_secret(self, secretName):
        raise NotImplementedError('Target engine does not implement the method')
    