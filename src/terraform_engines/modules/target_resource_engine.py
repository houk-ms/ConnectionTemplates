from typing import List
from payloads.binding import Binding
from terraform_engines.modules.base_resource_engine import BaseResourceEngine

class TargetResourceEngine(BaseResourceEngine):
    def __init__(self, template_path: str) -> None:
        super().__init__(template_path)

    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        raise NotImplementedError('Resource engine does not implement the method')

    # return the secrets to be stored in key vault
    def get_store_secrets(self) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')
    
    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')
    
    # return the app settings needed by http connection
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')

    def get_secret_value(self):
        pass