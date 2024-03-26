from typing import List
from payloads.resources.app_service import AppServiceResource

from engines.models.template import Template
from engines.modules.setting_resource_engine import SettingResourceEngine

from helpers import string_helper

class ContainerAppSettingsEngine(SettingResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        super().__init__(Template.CONTAINER_APP_BICEP.value,
                         Template.CONTAINER_APP_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('containerAppSettings', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('container-app-settings', self.resource.name)
        self.module_params_name = string_helper.format_camel('containerApp', self.resource.name, "Name")

