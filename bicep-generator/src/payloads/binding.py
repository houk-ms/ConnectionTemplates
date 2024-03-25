from payloads.models.connection_type import ConnectionType
from payloads.resource import Resource

class Binding():
    def __init__(self):
        self.source = None
        self.target = None
        self.connection = None
        self.store = None
        self.key = None
    
    def from_json(json, resources):
        binding = Binding()
        binding.source = Resource.from_expression(json['source'], resources)
        binding.target = Resource.from_expression(json['target'], resources)
        binding.store = Resource.from_expression(json.get('store'), resources)
        binding.connection = ConnectionType(json['connection'])
        binding.key = json.get('key')
        return binding
