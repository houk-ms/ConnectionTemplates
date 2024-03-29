from typing import List
from payloads.resources.function_app import FunctionAppResource

from bicep_engines.models.template import Template
from bicep_engines.modules.setting_resource_engine import SettingResourceEngine

from helpers import string_helper

class FunctionAppSettingsEngine(SettingResourceEngine):
    def __init__(self, resource: FunctionAppResource) -> None:
        super().__init__(Template.FUNCTION_APP_SETTINGS_BICEP.value,
                        Template.FUNCTION_APP_SETTINGS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('functionAppSettings', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('function-app-settings', self.resource.name)
        self.module_params_app_name = string_helper.format_camel('functionapp', self.resource.name, "Name")

