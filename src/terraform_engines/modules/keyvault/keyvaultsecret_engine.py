from typing import List
from payloads.binding import Binding
from payloads.resources.base_resource import BaseResource
from payloads.resources.keyvault import KeyVaultResource

from terraform_engines.models.appsetting import AppSetting, AppSettingType
from terraform_engines.models.template import Template
from terraform_engines.modules.base_resource_engine import BaseResourceEngine

from helpers import string_helper
from helpers.abbrevation import Abbreviation



class KeyVaultSecretEngine(BaseResourceEngine):

    def __init__(self, resource: BaseResource, keyvault: KeyVaultResource, app_setting_key: str, secret_value: str, index: int) -> None:
        super().__init__(Template.KEYVAULTSECRET_TF.value)
        self.resource = resource

        index = str(index) if index > 0 else ''
        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.KEYVAULT_SECRET.value, self.resource.type, self.resource.name, index)
        self.module_params_name = (self.resource.type + self.resource.name + index or Abbreviation.KEYVAULT_SECRET.value) + '${var.resource_suffix}'
        self.module_params_value = secret_value
        self.module_params_key_vault_id = 'azurerm_key_vault.{}.id'.format(string_helper.format_snake(Abbreviation.KEYVAULT.value, keyvault.name))
        self.app_setting_key = app_setting_key

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('key', 'vault', 'secret', self.resource.type, self.resource.name, 'id'), 
                'azurerm_key_vault_secret.{}.id'.format(self.module_name))
        ]

    def get_secret_id(self):
        return 'azurerm_key_vault_secret.{}.id'.format(self.module_name)
    
    def get_app_settings(self) -> List[tuple]:
        return [
            AppSetting(AppSettingType.KeyVaultReference, self.app_setting_key, self.get_secret_id()) # format in source template
        ]
