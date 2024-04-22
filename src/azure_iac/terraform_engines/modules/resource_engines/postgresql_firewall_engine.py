from azure_iac.payloads.resources.postgresql_db import PostgreSqlDbResource
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class PostgreSqlDbFirewallEngine(FirewallResourceEngine):

    def __init__(self, resource: PostgreSqlDbResource) -> None:
        super().__init__(Template.POSTGRESQL_FIREWALL_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.POSTGRESQL_DB.value, self.resource.name, 'rule')
        self.module_params_name = (self.resource.name or Abbreviation.POSTGRESQL_DB.value) + '${var.resource_suffix}' + '-allowAzure-rule'
        self.params_parent_module_name = string_helper.format_snake(Abbreviation.POSTGRESQL_DB.value, self.resource.name)