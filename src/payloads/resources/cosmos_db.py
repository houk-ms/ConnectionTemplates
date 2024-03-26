from payloads.models.resource_type import ResourceType

# TODO: database types
class CosmosDBResource():
    def __init__(self):
        self.type = ResourceType.AZURE_COSMOS_DB
        self.name = ''
    
    def from_json(json):
        result = CosmosDBResource()
        result.name = json.get('name', '')
        return result