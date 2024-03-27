from payloads.models.resource_type import ResourceType
from payloads.resources.base_resource import BaseResource

class SqlDbResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_SQL_DB
        self.name = ''
    
    def from_json(json):
        result = SqlDbResource()
        result.name = json.get('name', '')
        return result