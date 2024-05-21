from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.static_web_app import StaticWebAppResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation

class StaticWebAppEngine(SourceResourceEngine, TargetResourceEngine):
    # use linux web app as default
    def __init__(self, resource: StaticWebAppResource) -> None:
        SourceResourceEngine.__init__(self, Template.STATIC_WEB_APP_TF.value)
        TargetResourceEngine.__init__(self, Template.STATIC_WEB_APP_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.STATIC_WEB_APP.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.STATIC_WEB_APP.value) + '${var.resource_suffix}'

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('static', 'web', 'app', self.resource.name, 'id'), 
             'azurerm_static_web_app.{}.id'.format(self.module_name))
        ]

        # dependency engines
        self.depend_engines = []
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_key = 'SERVICE_URL'
        custom_key = custom_keys.get(default_key, default_key)
        if custom_key == default_key:
            custom_key = "SERVICE{}_URL".format(self.resource.name.upper())
        return [
            AppSetting(AppSettingType.KeyValue, custom_key, 'azurerm_static_web_app.{}.default_host_name'.format(self.module_name))
        ]
