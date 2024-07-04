from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class UserIdentityResource(BaseResource):
    def __init__(self, name=''):
        self.type = ResourceType.AZURE_USER_IDENTITY
        self.name = name
    
    def from_json(json):
        result = UserIdentityResource()
        result.name = json.get('name', '')
        return result