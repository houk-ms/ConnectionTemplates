from typing import List

from azure_iac.helpers.connection_info import RedisConnInfoHelper
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
        
        params_name = string_helper.format_resource_name(self.resource.name or Abbreviation.REDIS_CACHE.value)
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', params_name)
        ]
        self.main_outputs = [
            (string_helper.format_camel('redis', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]

    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        connInfoHelper = RedisConnInfoHelper("" if binding.source.service is None else binding.source.service.language)
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection,
                                             "bicep")
        
        return self._get_app_settings(configs)