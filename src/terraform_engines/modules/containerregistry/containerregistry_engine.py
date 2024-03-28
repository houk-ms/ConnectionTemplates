from payloads.resources.container_app import ContainerAppResource

from helpers.abbrevation import Abbreviation
from terraform_engines.models.template import Template
from terraform_engines.modules.base_resource_engine import BaseResourceEngine

from helpers import string_helper


class ContainerRegistryEngine(BaseResourceEngine):
    def __init__(self, resource: ContainerAppResource) -> None:
        super().__init__(Template.CONTAINER_REGISTRY_BICEP.value,
                         Template.CONTAINER_REGISTRY_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = 'containerRegistry'

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            ('containerRegistryName', 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.CONTAINER_REGISTRY.value)),
        ]
