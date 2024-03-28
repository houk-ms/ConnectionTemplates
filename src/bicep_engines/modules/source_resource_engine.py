from typing import List
from bicep_engines.modules.base_resource_engine import BaseResourceEngine


class SourceResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource.module states and variables
        self.module_var_principal_id_name = ''
        self.module_var_outbound_ip_name = ''

    # return the principal id variable name of current engine
    def get_identity_id(self) -> str:
        return self.module_var_principal_id_name
    
    # return the public ip variable name of current engine
    def get_outbound_ip(self) -> str:
        return self.module_var_outbound_ip_name
