from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class StaticWebAppResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_STATIC_WEB_APP
        self.name = ''
    
    def from_json(json):
        result = StaticWebAppResource()
        result.name = json.get('name', '')
        return result