from typing import List
from engines.modules.base_resource_engine import BaseResourceEngine

class SettingResourceEngine(BaseResourceEngine):
    def __init__(self,
                 bicep_template: str,
                 module_template: str) -> None:
        super().__init__(bicep_template, module_template)

        # resource.module states and variables
        self.module_params_app_settings = []


    # add app settings to the resource of current engine
    def add_app_settings(self, app_settings: List[tuple]) -> None:
        self.module_params_app_settings.extend(app_settings)