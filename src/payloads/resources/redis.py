from payloads.models.resource_type import ResourceType
from payloads.resources.base_resource import BaseResource

class RedisResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_REDIS_CACHE
        self.name = ''
    
    def from_json(json):
        result = RedisResource()
        result.name = json.get('name', '')
        return result