from typing import List

from azure_iac.bicep_engines.models.appsetting import AppSetting
from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine


class SettingResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource.module states and variables
        self.module_params_app_settings = []


    # add app settings to the resource of current engine
    def add_app_settings(self, app_settings: List[AppSetting]) -> None:
        # add and deduplicate app settings
        existing_setting_names = [setting.name for setting in self.module_params_app_settings]
        for app_setting in app_settings:
            if app_setting.name not in existing_setting_names:
                self.module_params_app_settings.append(app_setting)
