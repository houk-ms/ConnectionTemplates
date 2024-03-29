from typing import List

from payloads.binding import Binding
from payloads.resources.function_app import FunctionAppResource

from helpers.abbrevation import Abbreviation
from bicep_engines.models.appsetting import AppSetting, AppSettingType
from bicep_engines.models.template import Template
from bicep_engines.modules.source_resource_engine import SourceResourceEngine
from bicep_engines.modules.target_resource_engine import TargetResourceEngine
from bicep_engines.modules.functionappplan.functionappplan_engine import FunctionAppPlanEngine

from helpers import string_helper


class FunctionAppEngine(SourceResourceEngine, TargetResourceEngine):
    def __init__(self, resource: FunctionAppResource) -> None:
        SourceResourceEngine.__init__(self,
                                      Template.FUNCTION_APP_BICEP.value,
                                      Template.FUNCTION_APP_MODULE.value)
        TargetResourceEngine.__init__(self,
                                      Template.FUNCTION_APP_BICEP.value,
                                      Template.FUNCTION_APP_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('functionapp', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('function-app', self.resource.name)
        self.module_params_name = string_helper.format_camel('functionapp', self.resource.name, "Name")
        self.module_var_principal_id_name = '{}.outputs.identityPrincipalId'.format(self.module_name)
        self.module_var_outbound_ip_name = '{}.outputs.outboundIps'.format(self.module_name)

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.FUNCTION_APP.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('functionapp', self.resource.name, "Id"),
             'string', '{}.outputs.id'.format(self.module_name))]

        # dependency engines
        self.depend_engines = [
            FunctionAppPlanEngine(self.resource)
        ]

    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key, 
                '{}.outputs.requestUrl'.format(self.module_name))
        ]
