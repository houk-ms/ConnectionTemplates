from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.redis import RedisResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class RedisEngine(TargetResourceEngine):

    def __init__(self, resource: RedisResource) -> None:
        super().__init__(Template.REDIS_BICEP.value,
                         Template.REDIS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('redis', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('redis', self.resource.name)
        self.module_params_name = string_helper.format_camel('redis', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('redis', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.REDIS_CACHE.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('redis', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]

    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding, language: str) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_REDIS_CONNECTIONSTRING'
        
        return [
            AppSetting(AppSettingType.KeyVaultReference, app_setting_key,
                '{}.outputs.keyVaultSecretUri'.format(self.module_name))
        ]