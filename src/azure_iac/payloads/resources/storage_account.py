from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class StorageAccountResource(BaseResource):
    def __init__(self, name=''):
        self.type = ResourceType.AZURE_STORAGE_ACCOUNT
        self.name = name
    
    def from_json(json):
        result = StorageAccountResource()
        result.name = json.get('name', '')
        return result