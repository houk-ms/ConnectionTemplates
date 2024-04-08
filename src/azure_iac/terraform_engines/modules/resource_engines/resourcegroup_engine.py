from azure_iac.payloads.resources.app_service import AppServiceResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class ResourceGroupEngine(BaseResourceEngine):
    def __init__(self) -> None:
        super().__init__(Template.RESOURCE_GROUP_TF.value)
        self.resource = None

        # resource.module states and variables
        self.module_name = 'rg'
        self.module_params_name = Abbreviation.RESOURCE_GROUP + '${var.resource_suffix}'

        # main.tf variables and outputs
        self.main_variables = [
            ('resource_suffix', string_helper.get_random_str(5)),
            ('location', 'eastus'),
        ]
