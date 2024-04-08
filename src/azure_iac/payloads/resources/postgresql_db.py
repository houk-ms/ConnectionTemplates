from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class PostgreSqlDbResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_POSTGRESQL_DB
        self.name = ''
    
    def from_json(json):
        result = PostgreSqlDbResource()
        result.name = json.get('name', '')
        return result