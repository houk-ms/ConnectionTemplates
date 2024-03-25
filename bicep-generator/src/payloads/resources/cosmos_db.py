from payloads.models.resource_type import ResourceType

class CosmosDBResource():
    def __init__(self):
        self.type = ResourceType.AZURE_COSMOS_DB
        self.name = None
    
    def from_json(json):
        result = CosmosDBResource()
        result.name = json['name']
        return result