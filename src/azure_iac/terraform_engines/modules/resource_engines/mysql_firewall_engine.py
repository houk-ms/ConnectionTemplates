from azure_iac.payloads.resources.mysql_db import MySqlDbResource
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class MySqlDbFirewallEngine(FirewallResourceEngine):

    def __init__(self, resource: MySqlDbResource) -> None:
        super().__init__(Template.MYSQL_DB_FIREWALL_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.MYSQL_DB.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.MYSQL_DB.value) + '${var.resource_suffix}' + '-rule'
        self.params_parent_module_name = string_helper.format_snake(Abbreviation.MYSQL_DB.value, self.resource.name)