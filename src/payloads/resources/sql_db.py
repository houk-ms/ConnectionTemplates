from payloads.models.resource_type import ResourceType

class SqlDbResource():
    def __init__(self):
        self.type = ResourceType.AZURE_SQL_DB
        self.name = ''
    
    def from_json(json):
        result = SqlDbResource()
        result.name = json.get('name', '')
        return result