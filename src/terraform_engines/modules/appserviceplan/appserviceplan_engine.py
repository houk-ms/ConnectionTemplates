from payloads.resources.app_service import AppServiceResource

from helpers.abbrevation import Abbreviation
from terraform_engines.models.template import Template
from terraform_engines.modules.base_resource_engine import BaseResourceEngine

from helpers import string_helper


class AppServicePlanEngine(BaseResourceEngine):
    def __init__(self, resource: AppServiceResource, os_type: str) -> None:
        super().__init__(Template.APP_SERVICE_PLAN_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = Abbreviation.APP_SERVICE_PLAN.value + os_type.lower()
        self.module_params_name = Abbreviation.APP_SERVICE_PLAN.value + os_type.lower() + '${var.resource_suffix}'
        self.module_params_os_type = os_type

