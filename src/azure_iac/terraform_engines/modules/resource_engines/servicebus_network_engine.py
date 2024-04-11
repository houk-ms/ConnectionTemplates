from azure_iac.payloads.resources.service_bus import ServiceBusResource
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation

# `azurerm_servicebus_namespace_network_rule_set`` will be removed in version 4.0 of the AzureRM provider
class ServiceBusNetworkEngine(FirewallResourceEngine):

    def __init__(self, resource: ServiceBusResource) -> None:
        super().__init__(Template.SERVICE_BUS_NETWORK_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.SERVICE_BUS.value, self.resource.name)
        self.params_parent_module_name = string_helper.format_snake(Abbreviation.SERVICE_BUS.value, self.resource.name)