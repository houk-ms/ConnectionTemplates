from typing import List

from azure_iac.terraform_engines.models.appsetting import AppSetting
from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine


class SourceResourceEngine(BaseResourceEngine):
    def __init__(self, template_path: str) -> None:
        super().__init__(template_path)

        # resource module states and variables
        self.module_params_app_settings = []
        self.module_var_principal_id_name = ''
        self.module_var_outbound_ip_name = ''
        self.module_var_endpoint_name = ''

    # return the principal id variable name of current engine
    def get_identity_id(self) -> str:
        return self.module_var_principal_id_name
    
    # return the public ip variable name of current engine
    def get_outbound_ip(self) -> str:
        return self.module_var_outbound_ip_name

    # return the endpoint variable name of current engine
    def get_endpoint(self) -> str:
        return self.module_var_endpoint_name
    
    # add app settings to the resource of current engine
    def add_app_settings(self, app_settings: List[AppSetting]) -> None:
        # add and deduplicate app settings
        existing_setting_names = [setting.name for setting in self.module_params_app_settings]
        for app_setting in app_settings:
            if app_setting.name not in existing_setting_names:
                self.module_params_app_settings.append(app_setting)
