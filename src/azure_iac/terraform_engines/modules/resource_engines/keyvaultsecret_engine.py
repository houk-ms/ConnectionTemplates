from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType

from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation

class KeyVaultSecretEngine(BaseResourceEngine):

    def __init__(self, resource: TargetResourceEngine) -> None:
        super().__init__(Template.KEYVAULTSECRET_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(self.resource.type, self.resource.name)
        self.module_params_name = (self.resource.type + self.resource.name or Abbreviation.KEYVAULT_SECRET.value) + '${var.resource_suffix}'
        self.module_params_value = None
        self.module_params_key_vault_id = None

    # save the app setting value to keyvault secret (for SecretReference type) 
    # and change the app setting value to the secret id
    def change_appsettings_for_secret_reference(self, binding: Binding, app_settings: List[AppSetting]):
        for app_setting in app_settings:
            if app_setting.type == AppSettingType.SecretReference:
                # format the key vault id
                self.module_params_key_vault_id = 'azurerm_key_vault.{}.id'.format(
                    string_helper.format_snake(Abbreviation.KEYVAULT.value, binding.store.name))
                
                # save the app setting value as keyvault secret value
                self.module_params_value = app_setting.value
                
                # change the app setting value to the secret id
                app_setting.value = 'azurerm_key_vault_secret.{}.id'.format(self.module_name)
                # change the app setting type to use key vault reference format
                app_setting.type = AppSettingType.KeyVaultReference
