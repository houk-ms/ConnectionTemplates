from .base_engine import BaseEngine

# Target engine interface
class TargetEngine(BaseEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.need_existing_resource = False
    
    def generate_variables(self):
        self.set_variables()
        return super().generate_variables()
    
    def get_secret_name(self):
        raise NotImplementedError('Target engine does not implement the method')

    def get_app_settings(self):
        raise NotImplementedError('Target engine does not implement the method')
    
    def get_target_resource_id(self):
        raise NotImplementedError('Target engine does not implement the method')
    
    def set_variables(self):
        raise NotImplementedError('Target engine does not implement the method')