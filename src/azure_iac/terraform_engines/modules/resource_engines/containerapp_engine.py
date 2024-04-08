from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.container_app import ContainerAppResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.containerappenv_engine import ContainerAppEnvEngine
from azure_iac.terraform_engines.modules.resource_engines.containerregistry_engine import ContainerRegistryEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class ContainerAppEngine(SourceResourceEngine, TargetResourceEngine):
    def __init__(self, resource: ContainerAppResource) -> None:
        SourceResourceEngine.__init__(self, Template.CONTAINER_APP_TF.value)
        TargetResourceEngine.__init__(self, Template.CONTAINER_APP_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.CONTAINER_APP.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.CONTAINER_APP.value) + '${var.resource_suffix}'
        self.module_var_principal_id_name = 'azurerm_container_app.{}.identity.0.principal_id'.format(self.module_name)
        self.module_var_outbound_ip_name = 'azurerm_container_app.{}.outbound_ip_addresses'.format(self.module_name)

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('container', 'app', self.resource.name, 'id'), 
             'azurerm_container_app.{}.id'.format(self.module_name))
        ]
        
        self.container_registry = ContainerRegistryEngine(self.resource)

        # dependency engines
        self.depend_engines = [
            ContainerAppEnvEngine(self.resource),
            self.container_registry
        ]

    def get_identity_id(self) -> str:
        return super().get_identity_id()
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key,
                'azurerm_container_app.{}.ingress.0.fqdn'.format(self.module_name))
        ]

    def _get_module_params_secrets(self) -> List[tuple]:
        secrets = []
        for setting in self.module_params_app_settings:
            if not setting.is_raw_value():
                secrets.append((setting.secret_name, setting.value))
        
        # add the container registry password in secrets, not used in env
        secrets.append(('acr-password', 'azurerm_container_registry.{}.admin_password'.format(self.container_registry.module_name)))
        
        return secrets
        