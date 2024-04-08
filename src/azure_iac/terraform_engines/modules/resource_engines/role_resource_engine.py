from azure_iac.payloads.resources.base_resource import BaseResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine


class RoleResourceEngine(BaseResourceEngine):
    def __init__(self, resource: BaseResource) -> None:
        super().__init__(Template.ROLE_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = self.resource.type.value.lower() + self.resource.name
        self.module_params_principal_id = None
        self.module_params_scope = None
        self.module_params_role_definition_name = None

    # allow the principal to access the resource scope with the role definition
    def assign_role(self, principal_id: str, scope: str, role_definition_name: str) -> None:
        self.module_params_principal_id = principal_id
        self.module_params_scope = scope
        self.module_params_role_definition_name = role_definition_name
