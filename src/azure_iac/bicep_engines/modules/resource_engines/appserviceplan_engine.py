from azure_iac.payloads.resources.app_service import AppServiceResource

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class AppServicePlanEngine(BaseResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        super().__init__(Template.APP_SERVICE_PLAN_BICEP.value,
                         Template.APP_SERVICE_PLAN_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = 'appServicePlan'

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            ('appServicePlanName', 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.APP_SERVICE_PLAN.value)),
        ]
