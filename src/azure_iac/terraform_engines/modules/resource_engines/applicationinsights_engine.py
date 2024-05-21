from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.application_insights import ApplicationInsightsResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation



class ApplicationInsightsEngine(TargetResourceEngine):

    ApplicationInsightsComponentContributor = 'ae349356-3a1b-4a5e-921d-050484c6347e'

    def __init__(self, resource: ApplicationInsightsResource) -> None:
        super().__init__(Template.APP_INSIGHTS_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.APPLICATION_INSIGHTS.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.APPLICATION_INSIGHTS.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('application', 'insights', self.resource.name, 'id'), 
                'azurerm_application_insights.{}.id'.format(self.module_name))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_application_insights.{}.id'.format(self.module_name),
                ApplicationInsightsEngine.ApplicationInsightsComponentContributor)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        # TODO: use identity connection string
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.SecretReference, 'APPLICATIONINSIGHTS_CONNECTION_STRING', 'azurerm_application_insights.{}.connection_string'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.SecretReference, 'APPLICATIONINSIGHTS_CONNECTION_STRING', 'azurerm_application_insights.{}.connection_string'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]
