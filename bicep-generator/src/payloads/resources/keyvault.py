from payloads.models.resource_type import ResourceType

class KeyVaultResource():
    def __init__(self):
        self.type = ResourceType.AZURE_KEYVAULT
        self.name = None
    
    def from_json(json):
        result = KeyVaultResource()
        result.name = json['name']
        return result