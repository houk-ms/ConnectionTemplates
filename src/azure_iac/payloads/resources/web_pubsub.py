from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class WebPubSubResource(BaseResource):
    def __init__(self, name=''):
        self.type = ResourceType.AZURE_WEBPUBSUB
        self.name = name
    
    def from_json(json):
        result = WebPubSubResource()
        result.name = json.get('name', '')
        return result