from typing import List

from azure_iac.helpers.connection_info import ComputeResourceConnInfoHelper
from azure_iac.payloads.resources.static_web_app import StaticWebAppResource

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class StaticWebAppEngine(SourceResourceEngine, TargetResourceEngine):
    def __init__(self, resource: StaticWebAppResource) -> None:
        SourceResourceEngine.__init__(self,
                                      Template.STATIC_WEB_APP_BICEP.value,
                                      Template.STATIC_WEB_APP_MODULE.value)
        TargetResourceEngine.__init__(self,
                                      Template.STATIC_WEB_APP_BICEP.value,
                                      Template.STATIC_WEB_APP_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('staticWebApp', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('static-web-app', self.resource.name)
        self.module_params_name = string_helper.format_camel('staticWebApp', self.resource.name, "Name")

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.STATIC_WEB_APP.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('staticWebApp', self.resource.name, "Id"),
             'string', '{}.outputs.id'.format(self.module_name))]

        # dependency engines
        self.depend_engines = []
        
	
    def get_app_settings_http(self, binding):
        connInfoHelper = ComputeResourceConnInfoHelper("" if binding.source.service is None else binding.source.service['language'],
                                                       request_url='{}.outputs.requestUrl'.format(self.module_name),
                                                       resource_name=self.resource.name
                                                      )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection)
        
        return self._get_app_settings(configs)
