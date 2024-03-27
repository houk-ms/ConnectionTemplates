from payloads.models.resource_type import ResourceType
from payloads.resources.base_resource import BaseResource

# TODO: database types
class CosmosDBResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_COSMOS_DB
        self.name = ''
    
    def from_json(json):
        result = CosmosDBResource()
        result.name = json.get('name', '')
        return result