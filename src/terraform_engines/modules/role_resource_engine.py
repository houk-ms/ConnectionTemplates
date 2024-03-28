from terraform_engines.models.template import Template
from terraform_engines.modules.base_resource_engine import BaseResourceEngine


class RoleResourceEngine(BaseResourceEngine):
    def __init__(self) -> None:
        super().__init__(Template.ROLE_RESOURCE_TF.value)

        # resource module states and variables
        self.module_params_principal_id = None
        self.module_params_scope = None

    # allow the principal to access the resource scope with the role definition
    def assign_role(self, principal_id: str, scope: str, role_definition_id: str) -> None:
        self.module_params_principal_id = principal_id
        self.module_params_scope_props = scope
        self.module_params_role_definition_id = role_definition_id
