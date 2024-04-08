from payloads.resources.container_app import ContainerAppResource

from helpers.abbrevation import Abbreviation
from terraform_engines.models.template import Template
from terraform_engines.modules.base_resource_engine import BaseResourceEngine

class ContainerRegistryEngine(BaseResourceEngine):
    def __init__(self, resource: ContainerAppResource) -> None:
        super().__init__(Template.CONTAINER_REGISTRY_TF.value)
        self.resource = resource
        
        # resource module states and variables
        self.module_name = Abbreviation.CONTAINER_REGISTRY.value
        self.module_params_name = Abbreviation.CONTAINER_REGISTRY.value + '${var.resource_suffix}'
