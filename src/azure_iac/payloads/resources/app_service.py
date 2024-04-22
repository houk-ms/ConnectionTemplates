from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.compute_resource import ComputeResource


class AppServiceResource(ComputeResource):
    def __init__(self):
        super().__init__()

        self.type = ResourceType.AZURE_APP_SERVICE
        self.name = ''
    
    def from_json(json):
        result = AppServiceResource()
        result.name = json.get('name', '')
        return result