from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.aks import AKSResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.appserviceplan_engine import AppServicePlanEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class AKSEngine(SourceResourceEngine, TargetResourceEngine):
    # use linux web app as default
    def __init__(self, resource: AKSResource) -> None:
        SourceResourceEngine.__init__(self, Template.KUBERNETES_TF.value)
        TargetResourceEngine.__init__(self, Template.KUBERNETES_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.KUBERNETES.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.KUBERNETES.value) + '${var.resource_suffix}'
        self.module_var_principal_id_name = 'azurerm_kubernetes_cluster.{}.identity[0].principal_id'.format(self.module_name)
        # TODO: outbound ip

        if self.resource.settings:
            app_settings = []
            for setting in self.resource.settings:
                app_settings.append(AppSetting(AppSettingType.KeyValue, setting.get('name'), setting.get('value', '<...>')))
            self.add_app_settings(app_settings)

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('aks', self.resource.name, 'id'), 
             'azurerm_kubernetes_cluster.{}.id'.format(self.module_name))
        ]
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_key = 'SERVICE_URL'
        custom_key = custom_keys.get(default_key, default_key)
        if custom_key == default_key:
            custom_key = "SERVICE{}_URL".format(self.resource.name.upper())
        return [
            AppSetting(AppSettingType.KeyValue, custom_key, 'azurerm_kubernetes_cluster.{}.fqdn'.format(self.module_name))
        ]
    