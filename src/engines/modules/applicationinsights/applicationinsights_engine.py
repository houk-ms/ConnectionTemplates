from typing import List
from payloads.models.resource_type import ResourceType
from payloads.resources.application_insights import ApplicationInsightsResource

from engines.models.abbrevation import Abbreviation
from engines.models.template import Template
from engines.modules.target_resource_engine import TargetResourceEngine

from helpers import string_helper


class ApplicationInsightsEngine(TargetResourceEngine):
    def __init__(self, resource: ApplicationInsightsResource) -> None:
        super().__init__(Template.APP_INSIGHTS_BICEP.value,
                         Template.APP_INSIGHTS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('appInsights', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('app-insights', self.resource.name)
        self.module_params_name = string_helper.format_camel('appInsights', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('app-insights', self.resource.name)

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.APPLICATION_INSIGHTS.value)),
        ]

    # return the app settings needed by identity connection
    def get_app_settings_identity(self) -> List[tuple]:
        return [
            ('AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING', '{}.outputs.identityConnectionString'.format(self.module_name))
        ]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, compute: ResourceType) -> List[tuple]:
        if compute == ResourceType.AZURE_APP_SERVICE:
            return [
                ('AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING', '{}.outputs.appServiceSecretReference'.format(self.module_name))
            ]
        elif compute == ResourceType.AZURE_CONTAINER_APP:
            return [
                ('AZURE_APPLICATION_INSIGHTS_CONNECTION_STRING', '{}.outputs.containerAppSecretReference'.format(self.module_name))
            ]