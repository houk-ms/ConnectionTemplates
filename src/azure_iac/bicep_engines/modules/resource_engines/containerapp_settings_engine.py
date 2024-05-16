from typing import List

from azure_iac.payloads.resources.app_service import AppServiceResource
from azure_iac.payloads.models.project_type import ProjectType

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.setting_resource_engine import SettingResourceEngine

from azure_iac.helpers import string_helper


class ContainerAppSettingsEngine(SettingResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        super().__init__(Template.CONTAINER_APP_BICEP.value,
                         Template.CONTAINER_APP_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('containerAppSettings', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('container-app-settings', self.resource.name)
        self.module_params_name = string_helper.format_camel('containerApp', self.resource.name, "Name")
        if self.resource.projectType == ProjectType.AZD:
            self.module_params_service_name = self.resource.name
        self.module_params_target_port = self.resource.service.port

        if self.resource.settings:
            app_settings = []
            for setting in self.resource.settings:
                app_settings.append(
                    AppSetting(AppSettingType.KeyValue, setting.get('name'), "'{}'".format(setting.get('value', '<...>')))
                )
            self.add_app_settings(app_settings)
    
    def _get_module_params_secrets(self) -> List[tuple]:
        secrets = []
        for setting in self.module_params_app_settings:
            if not setting.is_raw_value():
                secrets.append((setting.secret_name, setting.value))
        return secrets
