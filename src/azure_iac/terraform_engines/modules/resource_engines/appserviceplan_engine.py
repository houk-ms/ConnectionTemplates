from azure_iac.payloads.resources.app_service import AppServiceResource

from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.terraform_engines.models.template import Template
from azure_iac.helpers.abbrevation import Abbreviation

class AppServicePlanEngine(BaseResourceEngine):
    def __init__(self, resource: AppServiceResource) -> None:
        super().__init__(Template.APP_SERVICE_PLAN_TF.value)
        self.resource = resource
        self.os_type = "Linux"

        # resource module states and variables
        self.module_name = Abbreviation.APP_SERVICE_PLAN.value + self.os_type.lower()
        self.module_params_name = Abbreviation.APP_SERVICE_PLAN.value + self.os_type.lower() + '${var.resource_suffix}'
        self.module_params_os_type = self.os_type

