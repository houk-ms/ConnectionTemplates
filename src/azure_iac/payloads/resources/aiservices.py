from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class AIServicesResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_AI_SERVICES
        self.name = ''
    
    def from_json(json):
        result = AIServicesResource()
        result.name = json.get('name', '')
        return result