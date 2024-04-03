from typing import List
from payloads.binding import Binding
from payloads.resources.app_service import AppServiceResource

from helpers.abbrevation import Abbreviation
from terraform_engines.models.appsetting import AppSetting, AppSettingType
from terraform_engines.models.template import Template
from terraform_engines.modules.source_resource_engine import SourceResourceEngine
from terraform_engines.modules.target_resource_engine import TargetResourceEngine
from terraform_engines.modules.appserviceplan.appserviceplan_engine import AppServicePlanEngine

from helpers import string_helper


class AppServiceLinuxEngine(SourceResourceEngine, TargetResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        SourceResourceEngine.__init__(self, Template.APP_SERVICE_LINUX_TF.value)
        TargetResourceEngine.__init__(self, Template.APP_SERVICE_LINUX_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.APP_SERVICE.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.APP_SERVICE.value) + '${var.resource_suffix}'
        self.module_var_principal_id_name = 'azurerm_linux_web_app.{}.identity[0].principal_id'.format(self.module_name)
        self.module_var_outbound_ip_name = 'azurerm_linux_web_app.{}.possible_outbound_ip_address_list'.format(self.module_name)

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('app', 'service', self.resource.name, 'id'), 
             'azurerm_linux_web_app.{}.id'.format(self.module_name))
        ]

        # dependency engines
        self.depend_engines = [
            AppServicePlanEngine(self.resource, "Linux"),
        ]

    def get_identity_id(self) -> str:
        return super().get_identity_id()
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key,
                '\"${{azurerm_linux_web_app.{}.name}}.azurewebsites.net\"'.format(self.module_name))
        ]
        