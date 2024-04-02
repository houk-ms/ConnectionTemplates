from typing import List

from bicep_engines.modules.storageaccount.storageaccount_engine import StorageAccountEngine
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
                string_helper.format_resource_name(self.resource.name or Abbreviation.FUNCTION_APP.value))
        ]
        self.main_outputs = [
            (string_helper.format_camel('functionapp', self.resource.name, "Id"),
             'string', '{}.outputs.id'.format(self.module_name))]

		# storage dependency
        self.storage = StorageAccountEngine(self.resource)

        # dependency engines
        self.depend_engines = [
            FunctionAppPlanEngine(self.resource),
            self.storage
        ]
        
        self.module_default_app_settings = self.get_default_app_settings()
        self.module_params_storage_name = self.storage.module_params_name

    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key, 
                '{}.outputs.requestUrl'.format(self.module_name))
        ]
    
    def get_default_app_settings(self):
        # required app settings
        default_settings = {
            'FUNCTIONS_WORKER_RUNTIME': '\'node\'',  # 'node', 'dotnet', 'java'
			'FUNCTIONS_EXTENSION_VERSION': '\'~4\'',
			'WEBSITE_NODE_DEFAULT_VERSION': '\'~14\'',
			# 'WEBSITE_CONTENTSHARE': 'toLower(name)', for Elastic Premium and Consumption plan
		}

        app_settings = [
            AppSetting(AppSettingType.FunctionAppSetting, key, value) for key, value in default_settings.items()	
		]

        storage_app_settings_name = ['AzureWebJobsStorage']  # 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING' for Elastic Premium and Consumption plan
        storage_app_settings_value = '\'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};AccountKey=${storageAccount.listKeys().keys[0].value};'
        api_types = ['Blob', 'Table', 'Queue', 'File']
        for api_type in api_types:
            storage_app_settings_value += '{}Endpoint=${{storageAccount.properties.primaryEndpoints.{}}};'.format(api_type, api_type.lower())
        storage_app_settings_value += '\''
        
        return app_settings + [
            AppSetting(AppSettingType.FunctionAppSetting, name, storage_app_settings_value) for name in storage_app_settings_name
		]
