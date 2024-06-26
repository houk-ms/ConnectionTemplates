from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.compute_resource import ComputeResource


class AKSResource(ComputeResource):
    def __init__(self):
        super().__init__()

        self.type = ResourceType.AZURE_KUBERNETES_SERVICE
        self.name = ''
    
    def from_json(json):
        result = AKSResource()
        result.name = json.get('name', '')
        return result