from payloads.models.resource_type import ResourceType

class ContainerAppResource():
    def __init__(self):
        self.type = ResourceType.AZURE_CONTAINER_APP
        self.name = None
    
    def from_json(json):
        result = ContainerAppResource()
        result.name = json['name']
        return result