from azure_iac.payloads.resources.storage_account import StorageAccountResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers.abbrevation import Abbreviation



class FunctionStorageEngine(TargetResourceEngine):

    def __init__(self, resource: StorageAccountResource) -> None:
        super().__init__(Template.FUNCTION_STORAGE_ACCOUNT_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = Abbreviation.STORAGE_ACCOUNT.value
        self.module_params_name = (self.resource.name or Abbreviation.STORAGE_ACCOUNT.value) + '${var.resource_suffix}'

