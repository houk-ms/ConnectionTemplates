from payloads.models.resource_type import ResourceType

class PostgreSqlDbResource():
    def __init__(self):
        self.type = ResourceType.AZURE_POSTGRESQL_DB
        self.name = None
    
    def from_json(json):
        result = PostgreSqlDbResource()
        result.name = json['name']
        return result