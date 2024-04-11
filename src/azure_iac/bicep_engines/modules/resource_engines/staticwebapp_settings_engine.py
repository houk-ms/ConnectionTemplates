from azure_iac.payloads.resources.static_web_app import StaticWebAppResource

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.setting_resource_engine import SettingResourceEngine

from azure_iac.helpers import string_helper


class StaticWebAppSettingsEngine(SettingResourceEngine):
    def __init__(self, resource: StaticWebAppResource) -> None:
        super().__init__(Template.STATIC_WEB_APP_SETTINGS_BICEP.value,
                        Template.STATIC_WEB_APP_SETTINGS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('staticWebAppSettings', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('static-web-app-settings', self.resource.name)
        self.module_params_app_name = string_helper.format_camel('staticWebApp', self.resource.name, "Name")

