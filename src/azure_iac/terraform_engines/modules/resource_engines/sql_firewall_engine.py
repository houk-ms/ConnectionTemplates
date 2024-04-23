from azure_iac.payloads.resources.sql_db import SqlDbResource
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class SqlDbFirewallEngine(FirewallResourceEngine):

    def __init__(self, resource: SqlDbResource) -> None:
        super().__init__(Template.SQL_DB_FIREWALL_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.SQL_DB.value, self.resource.name, 'rule')
        self.module_params_name = (self.resource.name or Abbreviation.SQL_DB.value) + '${var.resource_suffix}' + '-allowAzure-rule'
        self.params_parent_module_name = string_helper.format_snake(Abbreviation.SQL_DB.value, self.resource.name)
