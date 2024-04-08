from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class SpringAppResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_SPRING_APP
        self.name = ''
    
    def from_json(json):
        result = SpringAppResource()
        result.name = json.get('name', '')
        return result