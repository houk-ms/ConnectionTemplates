from azure_iac.payloads.resources.container_app import ContainerAppResource
from azure_iac.payloads.models.project_type import ProjectType

from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


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
                string_helper.format_resource_name(Abbreviation.CONTAINER_REGISTRY.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('containerRegistry', self.resource.name, "Id"), 'string',
             '{}.outputs.id'.format(self.module_name))]

        if self.resource.projectType == ProjectType.AZD:
            self.main_outputs.append(('AZURE_CONTAINER_REGISTRY_ENDPOINT', 'string',
             '{}.outputs.loginServer'.format(self.module_name)))
