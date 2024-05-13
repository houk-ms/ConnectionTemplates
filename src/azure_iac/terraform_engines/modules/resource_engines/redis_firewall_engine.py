from azure_iac.payloads.resources.redis import RedisResource
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class RedisFirewallEngine(FirewallResourceEngine):

    def __init__(self, resource: RedisResource) -> None:
        super().__init__(Template.REDIS_FIREWALL_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.REDIS_CACHE.value, self.resource.name, 'rule')
        self.module_params_name = (self.resource.name or Abbreviation.REDIS_CACHE.value) + '${var.resource_suffix}' + '_allowAzure_rule'
        self.params_parent_module_name = string_helper.format_snake(Abbreviation.REDIS_CACHE.value, self.resource.name)