from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class MySqlDbResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_MYSQL_DB
        self.name = ''
    
    def from_json(json):
        result = MySqlDbResource()
        result.name = json.get('name', '')
        return result