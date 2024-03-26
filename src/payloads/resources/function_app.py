from payloads.models.resource_type import ResourceType

class FunctionAppResource():
    def __init__(self):
        self.type = ResourceType.AZURE_FUNCTION_APP
        self.name = ''
    
    def from_json(json):
        result = FunctionAppResource()
        result.name = json.get('name', '')
        return result