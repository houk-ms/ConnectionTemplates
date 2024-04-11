from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.function_app import FunctionAppResource
from azure_iac.payloads.resources.storage_account import StorageAccountResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.bicep_engines.modules.resource_engines.functionappplan_engine import FunctionAppPlanEngine
from azure_iac.bicep_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation

from helpers import string_helper


class FunctionAppEngine(SourceResourceEngine, TargetResourceEngine):
    
    STORAGE_DEPENDENCY_NAME = "funcdep"

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
        self.module_var_endpoint_name = '{}.outputs.requestUrl'.format(self.module_name)

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.FUNCTION_APP.value))
        ]
        self.main_outputs = [
            (string_helper.format_camel('functionapp', self.resource.name, "Id"),
             'string', '{}.outputs.id'.format(self.module_name))]

        # dependency engines
        self.depend_engines = [
            FunctionAppPlanEngine(self.resource),
            StorageAccountEngine(StorageAccountResource(FunctionAppEngine.STORAGE_DEPENDENCY_NAME))
        ]
        
        self.module_default_app_settings = self.get_default_app_settings()
        self.module_params_storage_name = string_helper.format_camel('storageAccount', FunctionAppEngine.STORAGE_DEPENDENCY_NAME, "Name")

    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key, 
                '{}.outputs.requestUrl'.format(self.module_name))
        ]
    
    def get_default_app_settings(self):
        # function required app settings
        default_settings = {
            # TODO: runtime customizations, tier supports
            'FUNCTIONS_WORKER_RUNTIME': "'node'",
            'FUNCTIONS_EXTENSION_VERSION': "'~4'",
            'WEBSITE_NODE_DEFAULT_VERSION': "'~14'",
            'AzureWebJobsStorage': "'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};AccountKey=${storageAccount.listKeys().keys[0].value};"+
                "BlobEndpoint=${storageAccount.properties.primaryEndpoints.blob};"+
                "TableEndpoint=${storageAccount.properties.primaryEndpoints.table};"+
                "QueueEndpoint=${storageAccount.properties.primaryEndpoints.queue};"+
                "FileEndpoint=${storageAccount.properties.primaryEndpoints.file};'", 
        }

        return [
            AppSetting(AppSettingType.KeyValue, key, value) for key, value in default_settings.items()
        ]