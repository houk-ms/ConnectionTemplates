from payloads.models.resource_type import ResourceType

class SpringAppResource():
    def __init__(self):
        self.type = ResourceType.AZURE_SPRING_APP
        self.name = None
    
    def from_json(json):
        result = SpringAppResource()
        result.name = json['name']
        return result