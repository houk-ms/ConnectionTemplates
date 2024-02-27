from .target_engine import TargetEngine

# Role assignment engine interface
class RoleAssginmentEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)

    
    def set_module_param_principal_id(self, principal_id):
        raise NotImplementedError('Target engine does not implement the method')
    