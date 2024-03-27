from payloads.models.resource_type import ResourceType
from payloads.resources.base_resource import BaseResource

class ApplicationInsightsResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_APPLICATION_INSIGHTS
        self.name = ''
    
    def from_json(json):
        result = ApplicationInsightsResource()
        result.name = json.get('name', '')
        return result