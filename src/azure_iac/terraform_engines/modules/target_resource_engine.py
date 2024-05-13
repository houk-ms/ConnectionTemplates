from typing import List

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.payloads.binding import Binding
from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine


class TargetResourceEngine(BaseResourceEngine):
    def __init__(self, template_path: str) -> None:
        super().__init__(template_path)

    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        raise NotImplementedError('Resource engine {} does not implement the method'.format(self.__class__.__name__))

    # return the secrets to be stored in key vault
    def get_store_secrets(self) -> List[tuple]:
        raise NotImplementedError('Resource engine {} does not implement the method'.format(self.__class__.__name__))
    
    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        raise NotImplementedError('Resource engine {} does not implement the method'.format(self.__class__.__name__))
    
    # return the app settings needed by http connection
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        raise NotImplementedError('Resource engine {} does not implement the method'.format(self.__class__.__name__))
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        raise NotImplementedError('Resource engine {} does not implement the method'.format(self.__class__.__name__))
    
    def _get_app_settings(self, configs: List[tuple]):
        app_settings = []
        for app_setting_key, value, is_secret in configs:
            if is_secret:
                app_settings.append(
                    AppSetting(AppSettingType.SecretReference, app_setting_key, value)
                )
            else:
                app_settings.append(
                    AppSetting(AppSettingType.KeyValue, app_setting_key, value)
                )
        return app_settings
        