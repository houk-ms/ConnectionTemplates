from azure_iac.payloads.resources.container_app import ContainerAppResource

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class ContainerAppEnvEngine(BaseResourceEngine):
    def __init__(self, resource: ContainerAppResource) -> None:
        super().__init__(Template.CONTAINER_APP_ENV_BICEP.value,
                         Template.CONTAINER_APP_ENV_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = 'containerAppEnv'

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            ('containerAppEnvName', 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.CONTAINER_APP_ENV.value)),
        ]
