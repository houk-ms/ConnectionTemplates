from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.aisearch import AISearchResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


# TODO: firewall engine not supported yet
class AISearchEngine(TargetResourceEngine):

    SearchIndexDataContributor = 'Search Index Data Contributorr'

    def __init__(self, resource: AISearchResource) -> None:
        super().__init__(Template.AI_SEARCH_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.AI_SEARCH.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.AI_SEARCH.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('aisearch', self.resource.name, 'id'), 
                'azurerm_search_service.{}.id'.format(self.module_name))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_search_service.{}.id'.format(self.module_name),
                AISearchEngine.SearchIndexDataContributor)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        
        # TODO: TF does not support other endpoints for now, so we just concatenate the name
        name = 'azurerm_search_service.{}.name'.format(self.module_name) 
        deafult_settings = [
            (AppSettingType.KeyValue, 'AZURE_AISEARCH_ENDPOINT', '"https://${' + name + '}.search.windows.net/"'),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in deafult_settings]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys

        # TODO: TF does not support other endpoints for now, so we just concatenate the name
        name = 'azurerm_search_service.{}.name'.format(self.module_name) 
        deafult_settings = [
            (AppSettingType.KeyValue, 'AZURE_AISEARCH_ENDPOINT', '"https://${' + name + '}.search.windows.net/"'),
            (AppSettingType.KeyVaultReference, 'AZURE_AISEARCH_KEY', 'azurerm_search_service.{}.primary_key'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in deafult_settings]