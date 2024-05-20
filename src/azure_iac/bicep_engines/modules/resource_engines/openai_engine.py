from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.openai import OpenAIResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class OpenAIEngine(TargetResourceEngine):

    def __init__(self, resource: OpenAIResource) -> None:
        super().__init__(Template.OPENAI_BICEP.value,
                         Template.OPENAI_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('openAI', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('openai', self.resource.name)
        self.module_params_name = string_helper.format_camel('openAI', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('openai', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.OPENAI.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('openAI', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))
        ]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        deafult_settings = [
            (AppSettingType.KeyValue, 'AZURE_OPENAI_BASE', '{}.outputs.endpoint'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_OPENAI_DEPLOYMENT', '{}.outputs.deploymentName'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in deafult_settings]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        deafult_settings = [
            (AppSettingType.KeyValue, 'AZURE_OPENAI_BASE', '{}.outputs.endpoint'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_OPENAI_DEPLOYMENT', '{}.outputs.deploymentName'.format(self.module_name)),
            (AppSettingType.KeyVaultReference, 'AZURE_OPENAI_KEY', '{}.outputs.keyVaultSecretUri'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in deafult_settings]
