from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class KeyVaultResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_KEYVAULT
        self.name = ''
    
    def from_json(json):
        result = KeyVaultResource()
        result.name = json.get('name', '')
        return result