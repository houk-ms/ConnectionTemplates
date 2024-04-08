from azure_iac.payloads.resources.app_service import AppServiceResource

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.setting_resource_engine import SettingResourceEngine

from azure_iac.helpers import string_helper


class AppServiceSettingsEngine(SettingResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        super().__init__(Template.APP_SERVICE_SETTINGS_BICEP.value,
                        Template.APP_SERVICE_SETTINGS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('appServiceSettings', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('app-service-settings', self.resource.name)
        self.module_params_app_name = string_helper.format_camel('appService', self.resource.name, "Name")

