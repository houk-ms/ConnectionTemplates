from payloads.models.resource_type import ResourceType
from payloads.resources.base_resource import BaseResource

class AppServiceResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_APP_SERVICE
        self.name = ''
    
    def from_json(json):
        result = AppServiceResource()
        result.name = json.get('name', '')
        return result