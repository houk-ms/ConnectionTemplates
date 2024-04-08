from azure_iac.payloads.resources.storage_account import StorageAccountResource
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class StorageAccountFirewallEngine(FirewallResourceEngine):

    def __init__(self, resource: StorageAccountResource) -> None:
        super().__init__(Template.STORAGE_ACCOUNT_FIREWALL_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.STORAGE_ACCOUNT.value, self.resource.name)
        self.params_parent_module_name = string_helper.format_snake(Abbreviation.STORAGE_ACCOUNT.value, self.resource.name)