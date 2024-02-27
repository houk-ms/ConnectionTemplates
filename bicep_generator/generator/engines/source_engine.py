from .base_engine import BaseEngine

# Source engine interface
class SourceEngine(BaseEngine):
    def __init__(self, connector):
        super().__init__(connector)

    def get_principal_id(self):
        raise NotImplementedError('Target engine does not implement the method')
    

    def get_outbound_ip(self):
        raise NotImplementedError('Target engine does not implement the method')


    def set_variable_principal_id(self):
        raise NotImplementedError('Target engine does not implement the method')
    

    def set_variable_outbound_ip(self):
        raise NotImplementedError('Target engine does not implement the method')


    def set_module_param_app_settings(self, app_settings):
        raise NotImplementedError('Target engine does not implement the method')
    