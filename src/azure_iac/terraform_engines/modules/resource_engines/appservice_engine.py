from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.app_service import AppServiceResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.appserviceplan_engine import AppServicePlanEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class AppServiceEngine(SourceResourceEngine, TargetResourceEngine):
    # use linux web app as default
    def __init__(self, resource: AppServiceResource) -> None:
        SourceResourceEngine.__init__(self, Template.APP_SERVICE_LINUX_TF.value)
        TargetResourceEngine.__init__(self, Template.APP_SERVICE_LINUX_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.APP_SERVICE.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.APP_SERVICE.value) + '${var.resource_suffix}'
        self.module_var_principal_id_name = 'azurerm_linux_web_app.{}.identity[0].principal_id'.format(self.module_name)
        self.module_var_outbound_ip_name = 'azurerm_linux_web_app.{}.possible_outbound_ip_address_list'.format(self.module_name)
        # format the endpoint name rather than get it from output to avoid circular dependency
        self.module_var_endpoint_name = self.module_params_name + '.azurewebsites.net'

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('app', 'service', self.resource.name, 'id'), 
             'azurerm_linux_web_app.{}.id'.format(self.module_name))
        ]

        # dependency engines
        self.depend_engines = [
            AppServicePlanEngine(self.resource),
        ]
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key,
                'azurerm_linux_web_app.{}.default_hostname'.format(self.module_name))
        ]
    