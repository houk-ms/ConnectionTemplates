from azure_iac.helpers.abbrevation import Abbreviation
from azure_iac.payloads.resources.useridentity import UserIdentityResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine


class UserIdentityEngine(BaseResourceEngine):
    def __init__(self, resource: UserIdentityResource) -> None:
        super().__init__(Template.USER_IDENTITY_TF.value)
        
        self.resource = resource

        # resource module states and variables
        self.module_name = self.resource.name or Abbreviation.USER_IDENTITY.value
        self.module_params_name = (self.resource.name or Abbreviation.USER_IDENTITY.value) + '${var.resource_suffix}'

    def get_principal_id(self):
        return 'azurerm_user_assigned_identity.{}.principal_id'.format(self.module_name)
    
    def get_client_id(self):
        return 'azurerm_user_assigned_identity.{}.client_id'.format(self.module_name)
    
    def get_identity_id(self):
        return 'azurerm_user_assigned_identity.{}.id'.format(self.module_name)
