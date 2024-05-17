from typing import List

from azure_iac.helpers.connection_info import KeyVaultConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.keyvault import KeyVaultResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation



class KeyVaultEngine(TargetResourceEngine):

    KeyVaultSecretsOfficerRole = 'Key Vault Secrets Officer'

    def __init__(self, resource: KeyVaultResource) -> None:
        super().__init__(Template.KEYVAULT_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.KEYVAULT.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.KEYVAULT.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('storage', 'account', self.resource.name, 'id'), 
                'azurerm_key_vault.{}.id'.format(self.module_name))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_key_vault.{}.id'.format(self.module_name),
                KeyVaultEngine.KeyVaultSecretsOfficerRole)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        connInfoHelper = KeyVaultConnInfoHelper("" if binding.source.service is None else binding.source.service.language,
                                                resource_endpoint='azurerm_key_vault.{}.vault_uri'.format(self.module_name)
                                               )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection)
        
        return self._get_app_settings(configs)
