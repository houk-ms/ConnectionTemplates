from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class AISearchResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_AI_SEARCH
        self.name = ''
    
    def from_json(json):
        result = AISearchResource()
        result.name = json.get('name', '')
        return result