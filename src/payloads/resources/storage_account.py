from payloads.models.resource_type import ResourceType
from payloads.resources.base_resource import BaseResource

class StorageAccountResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_STORAGE_ACCOUNT
        self.name = ''
    
    def from_json(json):
        result = StorageAccountResource()
        result.name = json.get('name', '')
        return result