from payloads.models.connection_type import ConnectionType
from payloads.resource import Resource

class Binding():
    def __init__(self) -> None:
        self.source = None
        self.target = None
        self.connection = None
        self.store = None
        self.key = None
    
    def from_json(json: dict, all_resources: dict) -> 'Binding':
        binding = Binding()

        if 'source' not in json:
            raise ValueError(f'`source` property is not found in binding: {json}')
        binding.source = Resource.from_expression(json['source'], all_resources)

        if 'target' not in json:
            raise ValueError(f'`target` property is not found in binding: {json}')
        binding.target = Resource.from_expression(json['target'], all_resources)

        if 'connection' not in json:
            raise ValueError(f'`connection` property is not found in binding: {json}')
        binding.connection = ConnectionType(json['connection'])

        # optional properties
        if 'store' in json:
            binding.store = Resource.from_expression(json.get('store'), all_resources)
        binding.key = json.get('key')

        return binding
