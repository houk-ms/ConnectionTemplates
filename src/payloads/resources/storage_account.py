from payloads.models.resource_type import ResourceType

class StorageAccountResource():
    def __init__(self):
        self.type = ResourceType.AZURE_STORAGE_ACCOUNT
        self.name = ''
    
    def from_json(json):
        result = StorageAccountResource()
        result.name = json.get('name', '')
        return result