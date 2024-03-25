from typing import List
from payloads.models.resource_type import ResourceType
from engines.modules.base_resource_engine import BaseResourceEngine

class TargetResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource.module states and variables
        self.module_params_allow_ips = []
        self.module_params_principal_ids = []
        self.module_params_keyvault_name = ''
        self.module_params_secret_name = ''

    # save the target resource's secret to a keyvault secret
    def save_secret(self, kv_name: str) -> None:
        self.module_params_keyvault_name = kv_name
    
    # allow the principal to access the resource of current engine
    def assign_role(self, principal_id: str) -> None:
        self.module_params_principal_ids.append(principal_id)
    
    # allow the ip to access the resource of current engine
    def allow_firewall(self, public_ip: str) -> None:
        self.module_params_allow_ips.append(public_ip)
    
    # return the app settings needed by identity connection
    def get_app_settings_identity(self) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')
    
    # return the app settings needed by http connection
    def get_app_settings_http(self) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, compute: ResourceType) -> List[tuple]:
        raise NotImplementedError('Resource engine does not implement the method')
