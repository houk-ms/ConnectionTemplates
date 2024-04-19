from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.compute_resource import ComputeResource


class ContainerAppResource(ComputeResource):
    def __init__(self):
        self.type = ResourceType.AZURE_CONTAINER_APP
        self.name = ''
    
    def from_json(json):
        result = ContainerAppResource()
        result.name = json.get('name', '')
        return result