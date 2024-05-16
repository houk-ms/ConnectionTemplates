from azure_iac.payloads.resource import Resource
from azure_iac.payloads.models.resource_type import ResourceType


class Service():
    def __init__(self) -> None:
        self.host = None
        self.language = None
        self.project = None
        self.port = 80

    def from_json(json: dict, all_resources: dict) -> 'Service':
        service = Service()

        if 'host' not in json:
            raise ValueError(f'`host` property is not found in service: {json}')
        resource = Resource.from_expression(json['host'], all_resources)
        service.name = resource.name
        service.host = ResourceTypeToAzdServiceType[resource.type]
        service.port = json.get('port', 80)

        if 'language' not in json:
            raise ValueError(f'`language` property is not found in service: {json}')
        service.language = json['language']

        if 'project' not in json:
            raise ValueError(f'`project` property is not found in service: {json}')
        service.project = json['project']
        
        return service
    
    def get_identifier(self) -> str:
        return self.host.get_identifier()
    

ResourceTypeToAzdServiceType = {
    ResourceType.AZURE_CONTAINER_APP: 'containerapp',
    ResourceType.AZURE_FUNCTION_APP: 'function',
    ResourceType.AZURE_APP_SERVICE: 'appservice',
}