from payloads.resource import Resource

class Service():
    def __init__(self) -> None:
        self.host = None
        self.language = None
        self.project = None
    
    def from_json(json: dict, all_resources: dict) -> 'Service':
        result = Service()

        if 'host' not in json:
            raise ValueError(f'`host` property is not found in service: {json}')
        result.host = Resource.from_json(json['host'], all_resources)

        if 'language' not in json:
            raise ValueError(f'`language` property is not found in service: {json}')
        result.language = json['language']

        if 'project' not in json:
            raise ValueError(f'`project` property is not found in service: {json}')
        result.project = json['project']
        
        return result