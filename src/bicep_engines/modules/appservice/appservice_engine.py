from typing import List

from payloads.binding import Binding
from payloads.resources.app_service import AppServiceResource

from helpers.abbrevation import Abbreviation
from bicep_engines.models.appsetting import AppSetting, AppSettingType
from bicep_engines.models.template import Template
from bicep_engines.modules.source_resource_engine import SourceResourceEngine
from bicep_engines.modules.target_resource_engine import TargetResourceEngine
from bicep_engines.modules.appserviceplan.appserviceplan_engine import AppServicePlanEngine

from helpers import string_helper


class AppServiceEngine(SourceResourceEngine, TargetResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        SourceResourceEngine.__init__(self,
                                      Template.APP_SERVICE_BICEP.value,
                                      Template.APP_SERVICE_MODULE.value)
        TargetResourceEngine.__init__(self,
                                      Template.APP_SERVICE_BICEP.value,
                                      Template.APP_SERVICE_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('appService', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('app-service', self.resource.name)
        self.module_params_name = string_helper.format_camel('appService', self.resource.name, "Name")
        self.module_var_principal_id_name = '{}.outputs.identityPrincipalId'.format(self.module_name)
        self.module_var_outbound_ip_name = '{}.outputs.outboundIps'.format(self.module_name)

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.APP_SERVICE.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('appService', self.resource.name, "Id"),
             'string', '{}.outputs.id'.format(self.module_name))]

        # dependency engines
        self.depend_engines = [
            AppServicePlanEngine(self.resource)
        ]

    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key, 
                '{}.outputs.requestUrl'.format(self.module_name))
        ]
