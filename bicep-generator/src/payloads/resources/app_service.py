from payloads.models.resource_type import ResourceType

class AppServiceResource():
    def __init__(self):
        self.type = ResourceType.AZURE_APP_SERVICE
        self.name = None
    
    def from_json(json):
        result = AppServiceResource()
        result.name = json['name']
        return result