from payloads.resources.function_app import FunctionAppResource

from helpers.abbrevation import Abbreviation
from bicep_engines.models.template import Template
from bicep_engines.modules.base_resource_engine import BaseResourceEngine

from helpers import string_helper


class FunctionAppPlanEngine(BaseResourceEngine):
    def __init__(self, resource: FunctionAppResource) -> None:
        super().__init__(Template.FUNCTION_APP_PLAN_BICEP.value,
                         Template.FUNCTION_APP_PLAN_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = 'functionAppPlan'

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            ('functionAppPlanName', 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.APP_SERVICE_PLAN.value)),
        ]
