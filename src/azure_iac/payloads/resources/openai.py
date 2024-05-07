from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


# TODO: support database types
class OpenAIResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_OPENAI
        self.name = ''
    
    def from_json(json):
        result = OpenAIResource()
        result.name = json.get('name', '')
        return result