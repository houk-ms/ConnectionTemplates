from typing import List
from azure_iac.helpers.connection_info import RedisConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.redis import RedisResource

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
        connInfoHelper = RedisConnInfoHelper("" if binding.source.service is None else binding.source.service.language,
                                             connection_string='azurerm_redis_cache.{}.primary_connection_string'.format(self.module_name),
                                             host='azurerm_redis_cache.{}.hostname'.format(self.module_name),
                                             password='azurerm_redis_cache.{}.primary_access_key'.format(self.module_name),
                                             database=f'\"{self.module_params_database_name}\"',
                                             port='azurerm_redis_cache.{}.ssl_port'.format(self.module_name)
                                             )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection,
                                             "tf")
        return self._get_app_settings(configs)
