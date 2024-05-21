from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.function_app import FunctionAppResource
from azure_iac.payloads.resources.storage_account import StorageAccountResource
from azure_iac.payloads.resources.application_insights import ApplicationInsightsResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.appserviceplan_engine import AppServicePlanEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine
from azure_iac.terraform_engines.modules.resource_engines.applicationinsights_engine import ApplicationInsightsEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class FunctionAppEngine(SourceResourceEngine, TargetResourceEngine):
    # use linux web app as default
    def __init__(self, resource: FunctionAppResource) -> None:
        SourceResourceEngine.__init__(self, Template.FUNCTION_APP_LINUX_TF.value)
        TargetResourceEngine.__init__(self, Template.FUNCTION_APP_LINUX_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.FUNCTION_APP.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.FUNCTION_APP.value) + '${var.resource_suffix}'
        self.module_var_principal_id_name = 'azurerm_linux_function_app.{}.identity[0].principal_id'.format(self.module_name)
        self.module_var_outbound_ip_name = 'azurerm_linux_function_app.{}.possible_outbound_ip_address_list'.format(self.module_name)
        # format the endpoint name rather than get it from output to avoid circular dependency
        self.module_var_endpoint_name = self.module_params_name + '.azurewebsites.net'

        if self.resource.settings:
            app_settings = []
            for setting in self.resource.settings:
                app_settings.append(AppSetting(AppSettingType.KeyValue, setting.get('name'), setting.get('value', '<...>')))
            self.add_app_settings(app_settings)

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('function', 'app', self.resource.name, 'id'), 
             'azurerm_linux_function_app.{}.id'.format(self.module_name))
        ]

        # dependency engines
        self.depend_engines = [
            AppServicePlanEngine(self.resource),
            StorageAccountEngine(StorageAccountResource(name="funcdep")),
        ]
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_key = 'SERVICE_URL'
        custom_key = custom_keys.get(default_key, default_key)
        if custom_key == default_key:
            custom_key = "SERVICE{}_URL".format(self.resource.name.upper())
        return [
            AppSetting(AppSettingType.KeyValue, custom_key, 'azurerm_linux_function_app.{}.default_hostname'.format(self.module_name))
        ]
    