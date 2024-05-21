from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.application_insights import ApplicationInsightsResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class ApplicationInsightsEngine(TargetResourceEngine):
    def __init__(self, resource: ApplicationInsightsResource) -> None:
        super().__init__(Template.APP_INSIGHTS_BICEP.value,
                         Template.APP_INSIGHTS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('appInsights', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('app-insights', self.resource.name)
        self.module_params_name = string_helper.format_camel('appInsights', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('app-insights', self.resource.name)

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.APPLICATION_INSIGHTS.value)),
        ]

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[AppSetting]:        
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.KeyValue, 'APPLICATIONINSIGHTS_CONNECTION_STRING', '{}.outputs.identityConnectionString'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[AppSetting]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_key = 'APPLICATIONINSIGHTS_CONNECTION_STRING'
        if binding.store is not None:
            return [
                AppSetting(AppSettingType.KeyVaultReference, custom_keys.get(default_key, default_key),
                           '{}.outputs.keyVaultSecretUri'.format(self.module_name))
            ]
        else:
            return [
                AppSetting(AppSettingType.KeyValue, custom_keys.get(default_key, default_key),
                           '{}.outputs.ikeyConnectionString'.format(self.module_name))
            ]
