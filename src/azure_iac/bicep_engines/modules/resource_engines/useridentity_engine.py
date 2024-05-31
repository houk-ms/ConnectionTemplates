from typing import List

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation
from azure_iac.payloads.resources.useridentity import UserIdentityResource


class UserIdentityEngine(BaseResourceEngine):
    def __init__(self, resource: UserIdentityResource) -> None:
        super().__init__(Template.USER_IDENTITY_BICEP.value,
                       Template.USER_IDENTITY_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('userIdentity', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('user-identity', self.resource.name)
        self.module_params_name = string_helper.format_camel('userIdentity', self.resource.name, "Name")

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', string_helper.format_resource_name(self.resource.name or Abbreviation.USER_IDENTITY.value)),
        ]
        self.main_outputs = [
            ("userIdentityId", 'string', '{}.outputs.id'.format(self.module_name))
        ]

        # dependency engines
        self.depend_engines = []
        
	
    def get_principal_id(self) -> str:
        return '{}.outputs.identityPrincipalId'.format(self.module_name)


    def get_client_id(self):
        return '{}.outputs.identityClientId'.format(self.module_name)
    

    def get_identity_id(self) -> str:
        return '{}.outputs.id'.format(self.module_name)