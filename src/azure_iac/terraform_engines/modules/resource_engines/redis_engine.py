from typing import List

from azure_iac.helpers.constants import ClientType
from azure_iac.helpers.connection_info import get_client_type
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.redis import RedisResource

from azure_iac.terraform_engines.models.appsetting import AppSettingType, AppSetting
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class RedisEngine(TargetResourceEngine):
    def __init__(self, resource: RedisResource) -> None:
        super().__init__(Template.REDIS_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.REDIS_CACHE.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.REDIS_CACHE.value) + '${var.resource_suffix}'
        self.module_params_database_name = 'default'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('postgresql', 'server', self.resource.name, 'id'), 
             'azurerm_redis_cache.{}.id'.format(self.module_name))
        ]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.SecretReference, 'AZURE_REDIS_CONNECTIONSTRING', 'azurerm_redis_cache.{}.primary_connection_string'.format(self.module_name))
        ]
        separate_settings = [
            (AppSettingType.KeyValue, 'AZURE_REDIS_HOST', 'azurerm_redis_cache.{}.hostname'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_REDIS_DATABASE', f'\"{self.module_params_database_name}\"'),
            (AppSettingType.SecretReference, 'AZURE_REDIS_PASSWORD', 'azurerm_redis_cache.{}.primary_access_key'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_REDIS_PORT', 'azurerm_redis_cache.{}.ssl_port'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_REDIS_SSL', "\"true\"")
        ]
        client_type = get_client_type(binding.source.service.language)
        if client_type == ClientType.DEFAULT:
            return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in separate_settings]
        return [AppSetting(_type, key, value) for _type, key, value in default_settings]
