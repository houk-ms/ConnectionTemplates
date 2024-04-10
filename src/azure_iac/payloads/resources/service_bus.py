from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


# TODO: support choice between queue and topic
class ServiceBusResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_SERVICE_BUS
        self.name = ''
    
    def from_json(json):
        result = ServiceBusResource()
        result.name = json.get('name', '')
        return result